from datetime import datetime

# TODO: doc
def get_last_weights(db, table_name, num_weights=7):
    query = "SELECT * FROM {} ORDER BY date DESC LIMIT {}".format(table_name, num_weights)
    cursor = db.client.cursor()
    cursor.execute(query)

    weights = []
    for row in cursor.fetchall():
        weights.append(row_to_weight(row))

    cursor.close()
    return weights

# TODO: doc
def delete_by_date(db, table_name, date):
    date = format_date(date)
    query = "DELETE FROM {} WHERE date=%s".format(table_name)
    cursor = db.client.cursor()
    cursor.execute(query, (date,))
    db.client.commit()
    cursor.close()

# TODO: doc
def format_date(date=datetime.now()):
    return date.strftime("%Y-%m-%d")

def row_to_weight(row):
    return Weight(row[1], date=row[0], notes=row[2])

class Weight:
    def __init__(self, weight, date=datetime.now(), notes="", username="maxtrussell"):
        self.weight = weight
        self.date = format_date(date)
        self.notes = notes
        self.username = username

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

    

