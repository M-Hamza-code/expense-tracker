import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "..", "users.json")


def load_users():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            json.dump([], f)

    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_users(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)