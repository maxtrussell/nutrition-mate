# TODO: test, doc
from datetime import date, datetime, timedelta

import model.food as _food

# SELECT * FROM food_log INNER JOIN food ON (food_log.name=food.name) WHERE food_log.name="Apple";
def get_entries_by_day(db, log_table, food_table, start=date.today()):
    end = start + timedelta(days=1)
    query = (
            "SELECT * FROM {0} INNER JOIN {1} ON ({0}.name={1}.name) ".format(log_table, food_table) +
            "WHERE {}.time BETWEEN %s AND %s ORDER BY time DESC".format(log_table)
            )
    cursor = db.client.cursor()
    cursor.execute(query, (start, end))

    entries = []
    for entry in cursor.fetchall():
        entries.append(process_row(entry))

    cursor.close()
    return entries

def delete_entry(db, log_table, time):
    query = "DELETE FROM {} WHERE time=%s".format(log_table)
    cursor = db.client.cursor()
    cursor.execute(query, (time,))
    db.client.commit()
    cursor.close()

def process_row(row):
    food = _food.row_to_food(row[5:])
    logEntry = LogEntry(food, time=row[0], serving=row[2], quantity=row[3])
    return logEntry

class LogEntry:
    def __init__(
            self, food, time=datetime.now(), username="maxtrussell",
            quantity=0.0, serving="100g"
            ):
        self.food = food.normalize(target=quantity*food.servings[serving])
        self.time = time
        self.username = username
        self.quantity = quantity
        self.serving = serving

    def insert(self, db, table_name):
        """Inserts foode entry into MySQL table

        Parameters:
            database (db.db): MySQL database connection
            table_name (string): name of the table to insert into
        """
        query = (
                "INSERT INTO {}".format(table_name) +
                "(time, name, serving, quantity, username) VALUES " +
                "(%s, %s, %s, %s, %s)"
                )
        cursor = db.client.cursor()
        cursor.execute(query,
                (self.time, self.food.name, self.serving, self.quantity, self.username)
                )
        db.client.commit()
        cursor.close()


