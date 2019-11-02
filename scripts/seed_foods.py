import argparse
from getpass import getpass
import json
import requests
import typing as t

ENDPOINT = 'https://nutrition-mate.com/api/food'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', required=True)
    parser.add_argument('--username', '-u', required=True)
    args = parser.parse_args()

    with open(args.filename, 'r') as foods:
        for i in range(3):
            password = getpass()
            r = requests.post(
                ENDPOINT,
                json=json.load(foods),
                auth=requests.auth.HTTPBasicAuth(args.username, password),
            )
            if r.status_code != 401:
                break
            print('Sorry, try again.')
        r.raise_for_status()
    print('Sucessfully loaded foods :-)')

if __name__ == '__main__':
    main()
