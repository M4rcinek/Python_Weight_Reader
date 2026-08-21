import json
import os

APP_NAME = "WeightReader"
APPDATA_DIR = os.path.join(os.environ["LOCALAPPDATA"], APP_NAME)
SETTINGS_FILE = os.path.join(APPDATA_DIR, "settings.json")


DEFAULT_SETTINGS = {
    "port": "",
    "baudrate": "9600",
    "databits": "8",
    "parity": "None",
    "stopbits": "1"
}


def load_settings():
    os.makedirs(APPDATA_DIR, exist_ok=True)

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(data):
    os.makedirs(APPDATA_DIR, exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)