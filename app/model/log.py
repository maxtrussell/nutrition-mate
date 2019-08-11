# TODO: test, doc
from datetime import date, datetime, timedelta

import app.model.food as _food

def get_entries_by_day(db, log_table, food_table, start=date.today(), username=""):
    end = start + timedelta(days=1)
    query = (
            "SELECT * FROM {0} INNER JOIN {1} ON ({0}.food_id={1}.id AND {0}.username={1}.username) ".format(log_table, food_table) +
            "WHERE {0}.time >= %s AND {0}.time < %s AND {0}.username = %s ".format(log_table) +
            "ORDER BY time DESC"
            )
    cursor = db.client.cursor()
    cursor.execute(query, (start, end, username))

    entries = []
    for entry in cursor.fetchall():
        entries.append(process_row(entry))

    cursor.close()
    return entries

def delete_entry(db, log_table, time):
    query = "DELETE FROM {} WHERE id=%s".format(log_table)
    cursor = db.client.cursor()
    cursor.execute(query, (time,))
    db.client.commit()
    cursor.close()

def process_row(row):
    food = _food.row_to_food(row[6:])
    log_entry = LogEntry(food, id=row[0], time=row[1], serving=row[3], quantity=row[4])
    return log_entry

class LogEntry:
    def __init__(
            self, food, id=None, time=datetime.now(), username="",
            quantity=0.0, serving="100g"
            ):
        self.food = food.normalize(target=quantity*food.servings[serving])
        self.time = time
        self.username = username
        self.quantity = quantity
        self.serving = serving
        self.id = id

    def insert(self, db, table_name):
        """Inserts foode entry into MySQL table

        Parameters:
            database (db.db): MySQL database connection
            table_name (string): name of the table to insert into
        """
        query = (
                "INSERT INTO {}".format(table_name) +
                "(time, food_id, serving, quantity, username) VALUES " +
                "(%s, %s, %s, %s, %s)"
                )
        cursor = db.client.cursor()
        cursor.execute(query,
                (self.time, self.food.id, self.serving, self.quantity, self.username)
                )
        db.client.commit()
        cursor.close()


