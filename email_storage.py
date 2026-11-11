
import json
import os
from datetime import datetime


STORAGE_FOLDER = "email_data"
STORAGE_FILE = os.path.join(STORAGE_FOLDER, "email_history.json")


def save_email_history(email_history):
    os.makedirs(STORAGE_FOLDER, exist_ok=True)

    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            email_history,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_email_history():
    if not os.path.exists(STORAGE_FILE):
        return []

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def add_email_timestamp(email_data):
    email_data["submitted_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return email_data
