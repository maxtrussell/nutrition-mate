import pkg.config as config
import pkg.db.db as db

import json

class Food:
    def __init__(self, 
            name="",
            calories=0.0,
            fat=0.0,
            carbs=0.0,
            protein=0.0,
            alcohol=0.0,
            sugar=0.0,
            fiber=0.0,
            servings={},
            user="",
            ):
        self.name = name
        self.calories = calories
        self.fat = fat
        self.carbs = carbs
        self.protein = protein
        self.alcohol = alcohol
        self.sugar = sugar
        self.fiber = fiber
        self.servings = servings
        self.user = user

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
