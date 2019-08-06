from pkg.db import DB
import pkg.config as config

db = None

# Sets up mysql connection
def init():
    global db
    db = DB(
            config.values["mysql"]["username"],
            config.values["mysql"]["password"],
            config.values["mysql"]["host"],
            config.values["mysql"]["database"]
            )
