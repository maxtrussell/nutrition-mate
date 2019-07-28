import mysql.connector
from pkg.mock_db import MockClient

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
