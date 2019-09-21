import json
from pathlib import Path

GOOGLE_CREDENTIALS_PATH = Path.home().joinpath('.google/feedly_backup_credentials.json')


def read_credentials_file():
    with open(GOOGLE_CREDENTIALS_PATH.as_posix(), 'r') as credentials_file:
        return json.load(credentials_file)


def main():
    credentials = read_credentials_file()
    print(credentials)


if __name__ == '__main__':
    main()
