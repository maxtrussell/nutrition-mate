import json
import typing as t

import app.model.food as _food

class Ingredient():
    def __init__(
        self,
        meal_id: int,
        food_id: int,
        quantity: int,
        serving_label: str,
    ):
        self.id = -1
        self.food = None
        self.meal_id = meal_id
        self.food_id = food_id
        self.quantity = quantity
        self.serving_label = serving_label

    def insert(self, db, table_name):
        query = (
                f"INSERT INTO {table_name} (meal_id, food_id, quantity, serving_label) "
                f"VALUES (%s, %s, %s, %s)"
                )
        cursor = db.client.cursor(dictionary=True)
        cursor.execute(query, (self.meal_id, self.food_id, self.quantity, self.serving_label))
        db.client.commit()
        cursor.close()

def get_by_meal_id(db, ingredients_table, food_table, meal_id) -> t.List[Ingredient]:
    query = (
        f"SELECT ingredients.*, food.name, food.calories, food.fat, food.carbs, "
        f"food.protein, food.alcohol, food.sugar, food.fiber, food.servings "
        f"FROM {ingredients_table} INNER JOIN {food_table} ON "
        f"{ingredients_table}.food_id = {food_table}.id "
        f"WHERE {ingredients_table}.meal_id = %s"
    )
    cursor = db.client.cursor(dictionary=True)
    cursor.execute(query, (meal_id,))
    results = cursor.fetchall()
    ingredients = []
    for result in results:
        ingredient = Ingredient(
            result["meal_id"],
            result["food_id"],
            result["quantity"],
            result["serving_label"],
        )
        ingredient.id = result["id"]
        ingredient.food = _food.Food(
            id=result["food_id"],
            name=result["name"],
            calories=result["calories"],
            fat=result["fat"],
            carbs=result["carbs"],
            protein=result["protein"],
            alcohol=result["alcohol"],
            sugar=result["sugar"],
            fiber=result["fiber"],
            servings=json.loads(result["servings"]),
        )
        ingredients.append(ingredient)
    cursor.close()
    return ingredients
