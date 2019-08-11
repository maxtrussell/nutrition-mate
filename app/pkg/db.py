import mysql.connector
from app.pkg.mock_db import MockClient


class DB:
    def __init__(self, username, password, host, database, mock=False):
        if mock:
            self.client = MockClient()
        else:
            self.client = mysql.connector.connect(
                host=host,
                user=username,
                passwd=password,
                database=database
            )


def get_db(config):
    db = DB(
        config.db.USERNAME,
        config.db.PASSWORD,
        config.db.HOST,
        config.db.DB
    )
    return db
