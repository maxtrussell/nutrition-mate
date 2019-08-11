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
    return User(row[1], row[2], id=row[0], password_hash=row[3])
    

class User(UserMixin):
    def __init__(self, username, email, id=None, password_hash=None):
        self.username = username
        self.email = email
        self.id = id
        self.password_hash = password_hash

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
