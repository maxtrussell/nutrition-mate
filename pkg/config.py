from pkg.gcp import SecretFetcher
import configparser

values = None

def load_config(conf_path):
    global values
    values = configparser.ConfigParser()
    values.read(conf_path)
    fetch_secrets()

def fetch_secrets():
    global values
    sf = SecretFetcher(
            values["gcp"]["creds"],
            values["gcp"]["bucket"],
            values["gcp"]["secret_dir"], 
    )

    for key in values["secrets"]:
        values["secrets"][key] = sf.fetch_secret(key)
