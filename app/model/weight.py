# TODO: doc
from datetime import datetime

def get_last_weights(db, table_name, num_weights=100, username=""):
    query = "SELECT * FROM {} WHERE username = %s ORDER BY date DESC LIMIT {}".format(table_name, num_weights)
    cursor = db.client.cursor()
    cursor.execute(query, (username,))

    weights = []
    for row in cursor.fetchall():
        weight = row_to_weight(row)
        weight.five_day_avg = get_rolling_average(db, table_name, weight.date, 5, username)
        weight.ten_day_avg = get_rolling_average(db, table_name, weight.date, 10, username)
        weights.append(weight)

    cursor.close()
    return weights

def get_rolling_average(db, table_name, start_date, num_days, username):
    query = "select avg(weight) from ( select * from {} WHERE date <= %s AND username = %s ORDER BY date DESC LIMIT %s  ) as T;".format(table_name)
    cursor = db.client.cursor()
    cursor.execute(query, (start_date, username, num_days))
    avg = cursor.fetchone()[0]
    cursor.close()
    return avg

def delete_by_id(db, table_name, id):
    query = "DELETE FROM {} WHERE id=%s".format(table_name)
    cursor = db.client.cursor()
    cursor.execute(query, (id,))
    db.client.commit()
    cursor.close()

def format_date(date=datetime.now()):
    return date.strftime("%Y-%m-%d")

def row_to_weight(row):
    return Weight(row[2], date=row[1], notes=row[3], id=row[0], username=row[4])

class Weight:
    def __init__(self, weight, date=datetime.now(), notes="", username="", id=-1):
        self.id = id
        self.weight = weight
        self.date = format_date(date)
        self.notes = notes
        self.username = username
        self.five_day_avg = 0.0
        self.ten_day_avg = 0.0

    def insert(self, db, table_name):
        """Inserts weight object into MySQL table

        Parameters:
            database (db.db): MySQL database connection
            table_name (string): name of the table to insert into
        """
        query = (
                "INSERT INTO {} ".format(table_name) +
                "(date, weight, notes, username) VALUES (%s, %s, %s, %s)"
                )
        cursor = db.client.cursor()
        cursor.execute(query, (self.date, self.weight, self.notes, self.username))
        db.client.commit()
        cursor.close()

    

