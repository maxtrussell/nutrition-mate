import unittest
from app.model.food import Food, row_to_food, get_all_foods, get_food, parse_servings
from app.model.food import delete_by_name
from app.pkg.db import DB

class TestFood(unittest.TestCase):
    def setUp(self):
        self.food = Food(
            name="Apple",
            calories=52.0,
            fat=0.2,
            carbs=14.0,
            protein=0.3,
            sugar=10.0,
            fiber=2.4,
            servings={"100g": 100, "1 medium": 182},
            user="maxtrussell"
        )

    def test_insert(self):
        mock_db = DB(
                "mock username",
                "mock password",
                "mock host",
                "mock database",
                mock=True
                )
        self.food.insert(mock_db, "mock table")
        self.assertEqual(mock_db.client.cursor_called, 1)
        self.assertEqual(mock_db.client.commit_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.execute_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.close_called, 1)
        expected_query = (
                "INSERT INTO mock table " +
                "(name, calories, fat, carbs, protein, alcohol, sugar, fiber, servings, username) " +
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        self.assertEqual(mock_db.client.mock_cursor.query, expected_query)
        expected_values = (         
                "Apple", 52.0, 0.2, 14.0, 0.3, 0.0, 10.0, 2.4,
                '{"100g": 100, "1 medium": 182}', "maxtrussell"
        )
        self.assertEqual(mock_db.client.mock_cursor.values, expected_values)

    def test_delete(self):
        mock_db = DB(
                "mock username",
                "mock password",
                "mock host",
                "mock database",
                mock=True
                )
        delete_by_name(mock_db, "mock table", "Apple")
        self.assertEqual(mock_db.client.cursor_called, 1)
        self.assertEqual(mock_db.client.commit_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.execute_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.close_called, 1)
        expected_query = "DELETE FROM mock table WHERE lower(name)=%s"
        self.assertEqual(mock_db.client.mock_cursor.query, expected_query)
        expected_values = ("apple",)
        self.assertEqual(mock_db.client.mock_cursor.values, expected_values)

    def test_update(self):
        mock_db = DB(
                "mock username",
                "mock password",
                "mock host",
                "mock database",
                mock=True
                )
        self.food.update(mock_db, "mock table")
        self.assertEqual(mock_db.client.cursor_called, 1)
        self.assertEqual(mock_db.client.commit_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.execute_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.close_called, 1)
        expected_query = (
                "UPDATE mock table SET calories=%s, fat=%s, carbs=%s, protein=%s, " +
                "alcohol=%s, sugar=%s, fiber=%s, servings=%s, username=%s " +
                "WHERE name=%s"
        )
        self.assertEqual(mock_db.client.mock_cursor.query, expected_query)
        expected_values = (
                52.0, 0.2, 14.0, 0.3, 0.0, 10.0, 2.4,
                '{"100g": 100, "1 medium": 182}', "maxtrussell",
                "Apple"
        )
        self.assertEqual(mock_db.client.mock_cursor.values, expected_values)

    def test_get_food(self):
        mock_db = DB(
                "mock username",
                "mock password",
                "mock host",
                "mock database",
                mock=True
                )
        output = get_food(mock_db, "mock table", "Apple")
        self.assertEqual(mock_db.client.mock_cursor.execute_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.close_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.fetchone_called, 1)
        expected_query = "SELECT * FROM mock table WHERE lower(name)=%s"
        self.assertEqual(mock_db.client.mock_cursor.query, expected_query)
        self.assertEqual(mock_db.client.mock_cursor.values, ("apple",))

    def test_get_all_foods(self):
        mock_db = DB(
                "mock username",
                "mock password",
                "mock host",
                "mock database",
                mock=True
                )
        outputs = get_all_foods(mock_db, "mock table")
        self.assertEqual(mock_db.client.mock_cursor.execute_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.close_called, 1)
        self.assertEqual(mock_db.client.mock_cursor.fetchall_called, 1)
        expected_query = "SELECT * FROM mock table LIMIT 100"
        self.assertEqual(mock_db.client.mock_cursor.query, expected_query)
        self.assertEqual(mock_db.client.mock_cursor.values, None)

    def test_row_to_food(self):
        row = (
                'Apple', 52.0, 0.2, 14.0, 0.3, 0.0, 10.0, 2.4,
                '{"100g": 100, "1 medium": 182}', 'maxtrussell'
        )
        output = row_to_food(row)
        self.assertEqual(output.name, self.food.name)
        self.assertEqual(output.calories, 52.0)
        self.assertEqual(output.fat, 0.2)
        self.assertEqual(output.carbs, 14.0)
        self.assertEqual(output.protein, 0.3)
        self.assertEqual(output.alcohol, 0.0)
        self.assertEqual(output.sugar, 10.0)
        self.assertEqual(output.fiber, 2.4)
        self.assertEqual(output.servings, self.food.servings)
        self.assertEqual(output.user, self.food.user)

    def test_normalize_double(self):
        output = self.food.normalize(current=50.0)
        self.assertEqual(output.name, self.food.name)
        self.assertEqual(output.calories, 104.0)
        self.assertEqual(output.fat, 0.4)
        self.assertEqual(output.carbs, 28.0)
        self.assertEqual(output.protein, 0.6)
        self.assertEqual(output.alcohol, 0.0)
        self.assertEqual(output.sugar, 20.0)
        self.assertEqual(output.fiber, 4.8)
        self.assertEqual(output.servings, self.food.servings)
        self.assertEqual(output.user, self.food.user)

    def test_normalize_half(self):
        output = self.food.normalize(target=50.0)
        self.assertEqual(output.name, self.food.name)
        self.assertEqual(output.calories, 26.0)
        self.assertEqual(output.fat, 0.1)
        self.assertEqual(output.carbs, 7.0)
        self.assertEqual(output.protein, 0.15)
        self.assertEqual(output.alcohol, 0.0)
        self.assertEqual(output.sugar, 5.0)
        self.assertEqual(output.fiber, 1.2)
        self.assertEqual(output.servings, self.food.servings)
        self.assertEqual(output.user, self.food.user)

    def test_normalize_do_nothing(self):
        output = self.food.normalize(current=50.0, target=50.0)
        self.assertEqual(output.name, self.food.name)
        self.assertEqual(output.calories, 52.0)
        self.assertEqual(output.fat, 0.2)
        self.assertEqual(output.carbs, 14.0)
        self.assertEqual(output.protein, 0.3)
        self.assertEqual(output.alcohol, 0.0)
        self.assertEqual(output.sugar, 10.0)
        self.assertEqual(output.fiber, 2.4)
        self.assertEqual(output.servings, self.food.servings)
        self.assertEqual(output.user, self.food.user)

    def test_parse_servings(self):
        self.assertEqual(parse_servings("   "), {"100g": 100, "1g": 1})
        self.assertEqual(parse_servings(""), {"100g": 100, "1g": 1})

        raw1 = "1 bagel : 250"
        output = parse_servings(raw1)
        self.assertEqual(len(output), 3)
        self.assertEqual(output["1 bagel"], 250.0)
        self.assertEqual(output["100g"], 100.0)

        raw2 = "1 bagel : 250,1 pint: 0.7     ,   1 bag:200"
        output = parse_servings(raw2)
        self.assertEqual(len(output), 5)
        self.assertEqual(output["1 bagel"], 250.0)
        self.assertEqual(output["1 pint"], 0.7)
        self.assertEqual(output["1 bag"], 200.0)
        self.assertEqual(output["100g"], 100.0)


if __name__ == "__main__":
    unittest.main()
