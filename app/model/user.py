from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

def get_user_by_username(db, table, username):
    return get_user_by(db, table, "username", username)

def get_user_by_email(db, table, email):
    return get_user_by(db, table, "email", email)

def get_user_by_id(db, table, id):
    return get_user_by(db, table, "id", id)

def get_user_by(db, table, col_name, col_val):
    query = "select * from {} where {}=%s".format(table, col_name)
    cursor = db.client.cursor()
    cursor.execute(query, (col_val,))
    try:
        row = cursor.fetchone()
        user = row_to_user(row)
    except:
        user = None
    cursor.close()
    return user

def row_to_user(row):
    return User(
        username=row[1],
        email=row[2],
        id=row[0],
        password_hash=row[3], 
        calories_goal=row[4],
        fat_goal=row[5],
        carbs_goal=row[6],
        protein_goal=row[7],
        fiber_goal=row[8],
        sugar_goal=row[9],
        usda_api_key=row[10],
        view_verified_foods=row[11],
    )
    

class User(UserMixin):
    def __init__(
        self,
        username,
        email,
        id=None,
        password_hash=None,
        calories_goal=None,
        fat_goal=None,
        carbs_goal=None,
        protein_goal=None,
        sugar_goal=None,
        fiber_goal=None,
        usda_api_key=None,
        view_verified_foods=True,
    ):
        self.username = username
        self.email = email
        self.id = id
        self.password_hash = password_hash
        self.calories_goal = calories_goal
        self.fat_goal = fat_goal
        self.carbs_goal = carbs_goal
        self.protein_goal = protein_goal
        self.sugar_goal = sugar_goal
        self.fiber_goal = fiber_goal
        self.usda_api_key = usda_api_key
        self.view_verified_foods = view_verified_foods

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def insert(self, db, table):
        query = "INSERT INTO {} (username, email, password_hash) VALUES (%s, %s, %s)".format(table)
        cursor = db.client.cursor()
        cursor.execute(query, (self.username, self.email, self.password_hash))
        db.client.commit()
        cursor.close()

    def update(self, db, table):
        query = (f"UPDATE {table} "
                 f"SET calories_goal = %s, "
                 f"fat_goal = %s, "
                 f"carbs_goal = %s, "
                 f"protein_goal = %s, "
                 f"sugar_goal = %s, "
                 f"fiber_goal = %s, "
                 f"usda_api_key = %s, "
                 f"view_verified_foods = %s "
                 f"WHERE username=%s"
        )
        cursor = db.client.cursor()
        cursor.execute(query, (
                self.calories_goal,
                self.fat_goal,
                self.carbs_goal,
                self.protein_goal,
                self.sugar_goal,
                self.fiber_goal,
                self.usda_api_key,
                self.view_verified_foods,
                self.username,
            )
        )
        db.client.commit()
        cursor.close()
