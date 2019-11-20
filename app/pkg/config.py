import os
import sys

from app.pkg.gcp import SecretFetcher

basedir = os.path.abspath(os.path.dirname(sys.argv[0]))


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
    USDA_API_KEY = ""
    ADMIN_USER_PASSWORD = ""


class Server:
    HOST = "0.0.0.0"
    PORT = "5001"
    ADMIN_EMAIL = "bogus@gmail.com"


class Config:
    gcp = GCP()
    db = MySQL()
    secrets = Secrets()
    server = Server()


def get_secrets(config):
    sf = SecretFetcher(config.gcp.CREDS, config.gcp.BUCKET,
                       config.gcp.SECRET_DIR)
    config.secrets.REGISTRATION_KEY = sf.fetch_secret("registration_key")
    config.secrets.USDA_API_KEY = sf.fetch_secret("usda_api_key")
    config.secrets.ADMIN_USER_PASSWORD = sf.fetch_secret("admin_user_password")
    return config
