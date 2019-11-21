import typing as t

import app.model.food as _food
import app.model.ingredient as ingredient

def get_by_id(db, table_name, id):
    query = f"SELECT * FROM {table_name} WHERE id=%s"
    cursor = db.client.cursor(dictionary=True)
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    meal = Meal(
        name=result["name"],
        username=result["username"],
        servings=result["servings"],
    )
    meal.id = result["id"]
    return meal

def get_by_username(db, table_name, username):
    query = f"SELECT * FROM {table_name} WHERE username=%s"
    cursor = db.client.cursor(dictionary=True)
    cursor.execute(query, (username,))
    results = cursor.fetchall()
    meals = []
    for result in results:
        meal = Meal(
            name=result["name"],
            username=result["username"],
            servings=result["servings"],
        )
        meal.id = result["id"]
        meals.append(meal)
    return meals

class Meal():
    def __init__(
        self,
        name: str,
        username: str,
        servings: int,
        ingredients: t.List[ingredient.Ingredient]=[],
    ):
        self.id = -1
        self.name = name
        self.username = username
        self.servings = servings
        self.ingredients = ingredients

    def insert(self, db, table_name):
        query = f"INSERT INTO {table_name} (name, username) VALUES (%s, %s)"
        cursor = db.client.cursor()
        cursor.execute(query, (self.name, self.username))
        db.client.commit()
        self.id = cursor.lastrowid
        cursor.close()
        return self.id
    
    def get_ingredients(self, db, ingredients_table, food_table):
        self.ingredients = ingredient.get_by_meal_id(db, ingredients_table, food_table, self.id)
        scaled_ingredients = [i.food.normalize(target=i.quantity) for i in self.ingredients]
        self.total = _food.Food(
            name="Total",
            calories = sum([f.calories for f in scaled_ingredients]),
            fat = sum([f.fat for f in scaled_ingredients]),
            carbs = sum([f.carbs for f in scaled_ingredients]),
            protein = sum([f.protein for f in scaled_ingredients]),
            alcohol = sum([f.alcohol for f in scaled_ingredients]),
            sugar = sum([f.sugar for f in scaled_ingredients]),
            fiber = sum([f.fiber for f in scaled_ingredients]),
        )

