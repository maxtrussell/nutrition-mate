from dataclasses import dataclass, field

from app.pkg.config import Config

import json

config = Config()

def get_all_foods(database, table_name, username="", show_verified=False):
    """Gets all foods from given MySQL table

    Parameters:
        database (db.DB): MySQL db object 
        table_name (string): name of MySQL table

    Returns:
        foods ([]Food): list of food objects from table
    """
    # send the query
    if show_verified:
        query = "SELECT * FROM {} WHERE username = %s OR username = %s LIMIT 100".format(table_name)
        cursor = database.client.cursor()
        cursor.execute(query, (username, "admin"))
    else:
        query = "SELECT * FROM {} WHERE username = %s LIMIT 100".format(table_name)
        cursor = database.client.cursor()
        cursor.execute(query, (username,))

    foods = []
    for row in cursor.fetchall():
        foods.append(row_to_food(row))

    cursor.close()
    return foods

def get_food(database, table_name, food_id, username="", show_verified=False):
    """Gets a food by id from a MySQL table

    Parameters:
        database (db.DB): MySQL db object 
        table_name (string): name of MySQL table
        food_name (string): name of food to query

    Returns:
        food (Food): food object from table
    """
    if show_verified:
        query = "SELECT * FROM {} WHERE id=%s AND (username=%s or username=%s)".format(table_name)
        cursor = database.client.cursor()
        cursor.execute(query, (food_id, username, "admin"))
    else:
        query = "SELECT * FROM {} WHERE id=%s AND username=%s".format(table_name)
        cursor = database.client.cursor()
        cursor.execute(query, (food_id, username))

    row = cursor.fetchone()
    food = row_to_food(row)

    cursor.close()
    return food

def search(db, table, search, username, show_verified=False):
    # limit search to five words for performance reasons
    s_words = search.split()[:5]

    all_results = []
    for word in s_words:
        word = "%" + word + "%"
        if show_verified:
            query = "SELECT * FROM {} WHERE (username=%s OR username=%s) AND lower(name) LIKE %s LIMIT 100".format(table)
            cursor = db.client.cursor()
            cursor.execute(query, (username, "admin", word.lower()))
        else:
            query = "SELECT * FROM {} WHERE username=%s AND lower(name) LIKE %s LIMIT 100".format(table)
            cursor = db.client.cursor()
            cursor.execute(query, (username, word.lower()))

        results = set()
        for row in cursor.fetchall():
            results.add(row_to_food(row))
        all_results.append(results)

    cursor.close()
    return list(set.intersection(*all_results))


def row_to_food(row):
    """Initializes a food item from a MySQL row

    Parameters:
        row (tuple): a tuple containing all attributes of food

    Returns:
        food (Food): a newly instantiated Food object
    """
    food = Food()
    food.name = row[1]
    food.calories = row[2]
    food.fat = row[3]
    food.carbs = row[4]
    food.protein = row[5]
    food.alcohol = row[6]
    food.sugar = row[7]
    food.fiber = row[8]
    food.servings = json.loads(row[9])
    food.user = row[10]
    food.id = row[0]
    return food

def parse_servings(raw):
    servings = {}
    pairs = raw.split(",")
    for pair in pairs:
        keyvals = pair.split(":")
        if len(keyvals) == 2:
            key = keyvals[0].strip()
            val = float(keyvals[1].strip())
            servings[key] = val
    return servings

def delete_by_id(database, table_name, id, username):
    """Delete food by id from MySQL table
    
    Parameters:
        database (db.db): MySQL database connection
        table_name (string): name of the table to delete from
    """
    query = "DELETE FROM {} WHERE username=%s AND id=%s".format(table_name)
    cursor = database.client.cursor()
    cursor.execute(query, (username, id))
    database.client.commit()
    cursor.close()

@dataclass()
class Food:
    name: str = ""
    calories: float = 0.0
    fat: float = 0.0
    carbs: float = 0.0
    protein: float = 0.0
    alcohol: float = 0.0
    sugar: float = 0.0
    fiber: float = 0.0
    servings: dict = field(default_factory=lambda: {})
    user: str = ""
    id: int = 0

    def __post_init__(self):
        self.servings["1g"] = 1
        self.servings["100g"] = 100
        if self.calories == 0.0:
            self.calories = self.calculate_calories()

    def __hash__(self):
        return self.id

    def calculate_calories(self):
        """Calculates calories from macro nutrients

        Returns:
            calories (float): number of calories in this food
        """
        return (self.fat*9 + self.carbs*4 + self.protein*4 +
                self.alcohol*7)

    def normalize(self, current=100.0, target=100.0):
        """Scales the nutrition info of a Food object
        e.g. current=1.0, target=2.0 would double all nutrition stats

        Parameters:
            current (float): how many grams there are currently of the food
            target (float): how many grams you want the nutrition food to be scaled to

        Returns:
            normalized (Food): The new normalized Food object
        """
        ratio = target/current
        normalized = Food(name=self.name, servings=self.servings, user=self.user, id=self.id)
        normalized.calories = ratio * self.calories
        normalized.fat = ratio * self.fat
        normalized.carbs = ratio * self.carbs
        normalized.protein = ratio * self.protein
        normalized.alcohol = ratio * self.alcohol
        normalized.sugar = ratio * self.sugar
        normalized.fiber = ratio * self.fiber
        return normalized

    def insert(self, database, table_name):
        """Inserts the Food object into a MySQL table
        
        Parameters:
            database (db.db): MySQL database connection
            table_name (string): name of the table to insert into
        """
        query = (
                "INSERT INTO {} ".format(table_name) + 
                "(name, calories, fat, carbs, protein, alcohol, sugar, fiber, servings, username) " +
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        cursor = database.client.cursor()
        cursor.execute(
                query, (
                    self.name, self.calories, self.fat,
                    self.carbs, self.protein, self.alcohol,
                    self.sugar, self.fiber, json.dumps(self.servings),
                    self.user
                )
        )
        database.client.commit()
        food_id = cursor.lastrowid
        cursor.close()
        return food_id

    def update(self, database, table_name):
        """Update food item in MySQL table

        Parameters:
            database (db.db): MySQL database connection
            table_name (string): name of the table to update in
        """
        query = (
                "UPDATE {} SET name=%s, calories=%s, fat=%s, carbs=%s, protein=%s, ".format(table_name) +
                "alcohol=%s, sugar=%s, fiber=%s, servings=%s " +
                "WHERE id=%s"
                )
        cursor = database.client.cursor()
        cursor.execute(
                query, (
                    self.name, self.calories, self.fat, self.carbs,
                    self.protein, self.alcohol, self.sugar, self.fiber,
                    json.dumps(self.servings), self.id
                )
        )
        database.client.commit()
        cursor.close()
    
    def serving_string(self):
        s = ""
        for key, val in self.servings.items():
            if key != "100g" and key != "1g":
                s += "{}: {}, ".format(key, val)
        # trim trailing comma and space
        s = s[:-2]
        return s

