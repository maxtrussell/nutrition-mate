from dataclasses import dataclass, field

import pkg.config as config

import json

def get_all_foods(database, table_name):
    """Gets all foods from given MySQL table

    Parameters:
        database (db.DB): MySQL db object 
        table_name (string): name of MySQL table

    Returns:
        foods ([]Food): list of food objects from table
    """
    # send the query
    query = "SELECT * FROM {} LIMIT 100".format(table_name)
    cursor = database.client.cursor()
    cursor.execute(query)

    foods = []
    for row in cursor.fetchall():
        foods.append(row_to_food(row))

    cursor.close()
    return foods

def get_food(database, table_name, food_name):
    """Gets a food by name from a MySQL table

    Parameters:
        database (db.DB): MySQL db object 
        table_name (string): name of MySQL table
        food_name (string): name of food to query

    Returns:
        food (Food): food object from table
    """
    query = "SELECT * FROM {} WHERE lower(name)=%s".format(table_name)
    cursor = database.client.cursor()
    cursor.execute(query, (food_name.lower(),))

    row = cursor.fetchone()
    food = row_to_food(row)

    cursor.close()
    return food

def search(db, table, search):
    search = "%" + search + "%"
    query = "SELECT * FROM {} WHERE lower(name) LIKE %s LIMIT 100".format(table)
    cursor = database.client.cursor()
    cursor.execute(query)

    foods = []
    for row in cursor.fetchall():
        foods.append(row_to_food(row))

    cursor.close()
    return foods


def row_to_food(row):
    """Initializes a food item from a MySQL row

    Parameters:
        row (tuple): a tuple containing all attributes of food

    Returns:
        food (Food): a newly instantiated Food object
    """
    food = Food()
    food.name = row[0]
    food.calories = row[1]
    food.fat = row[2]
    food.carbs = row[3]
    food.protein = row[4]
    food.alcohol = row[5]
    food.sugar = row[6]
    food.fiber = row[7]
    food.servings = json.loads(row[8])
    food.user = row[9]
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

def delete_by_name(database, table_name, food_name):
    """Delete food by name from MySQL table
    
    Parameters:
        database (db.db): MySQL database connection
        table_name (string): name of the table to delete from
    """
    query = "DELETE FROM {} WHERE lower(name)=%s".format(table_name)
    cursor = database.client.cursor()
    cursor.execute(query, (food_name.lower(),))
    database.client.commit()
    cursor.close()

# TODO: test
# TODO: use
def search(database, table_name, search_text):
    """Searches for foods from a MySQL table

    Parameters:
        database (db.DB): MySQL db object 
        table_name (string): name of MySQL table
        search_text (string): text to search for

    Returns:
        matches ([]Food): food object(s) from table
    """
    query = "SELECT * FROM {} WHERE lower(name) LIKE %s LIMIT 100".format(table_name)
    cursor = database.client.cursor()
    search_text = "%" + search_text + "%"
    cursor.execute(query, (search_text.lower(),))

    matches = []
    for row in cursor.fetchall():
        matches.append(row_to_food(row))

    cursor.close()
    return matches

@dataclass
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
    user: str = "maxtrussell"

    def __post_init__(self):
        self.servings["1g"] = 1
        self.servings["100g"] = 100
        if self.calories == 0.0:
            self.calories = self.calculate_calories()

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
        normalized = Food(name=self.name, servings=self.servings, user=self.user)
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
        cursor.close()

    def update(self, database, table_name):
        """Update food item in MySQL table

        Parameters:
            database (db.db): MySQL database connection
            table_name (string): name of the table to update in
        """
        query = (
                "UPDATE {} SET calories=%s, fat=%s, carbs=%s, protein=%s, ".format(table_name) +
                "alcohol=%s, sugar=%s, fiber=%s, servings=%s, username=%s " +
                "WHERE name=%s"
                )
        cursor = database.client.cursor()
        cursor.execute(
                query, (
                    self.calories, self.fat, self.carbs, self.protein,
                    self.alcohol, self.sugar, self.fiber, json.dumps(self.servings),
                    self.user, self.name
                )
        )
        database.client.commit()
        cursor.close()

