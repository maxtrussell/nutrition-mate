from google.cloud import storage
import os

class SecretFetcher:
    def __init__(self, creds, bucket, directory):
        self.client = storage.Client.from_service_account_json(creds)
        self.bucket = self.client.get_bucket(bucket)
        self.directory = directory
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    def fetch_secret(self, secret_name):
        blob = self.bucket.blob(secret_name)
        blob.download_to_filename(os.path.join(self.directory, secret_name))
        secret = ""
        with open(os.path.join(self.directory, secret_name), "r") as f:
            secret = f.read().strip()
        return secret

