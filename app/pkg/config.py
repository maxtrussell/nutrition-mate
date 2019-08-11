import os

basedir = os.path.abspath(os.path.dirname(__file__))


class GCP:
    CREDS = os.path.join(basedir, "external/gcp/creds.json")
    BUCKET = "nutrition-mate-secrets"
    SECRET_DIR = "secrets"


class MySQL:
    USERNAME = "maxtrussell"
    PASSWORD = ""
    HOST = "localhost"
    DB = "nm"
    FOODS = "food"
    WEIGHTS = "weight"
    LOG = "food_log"
    USERS = "users"


class Secrets:
    REGISTRATION_KEY = ""


class Server:
    HOST = "0.0.0.0"
    PORT = "5000"


class Config:
    gcp = GCP()
    db = MySQL()
    secrets = Secrets()
    server = Server()
