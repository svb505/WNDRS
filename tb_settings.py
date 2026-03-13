import json
import os

def save_settings(hotkey_screenshot, hotkey_record,SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({
            "hotkey_screenshot": hotkey_screenshot,
            "hotkey_record": hotkey_record
        }, f)
def load_settings(SETTINGS_FILE):
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f: return json.load(f)
    return {
        "hotkey_screenshot": "F9",
        "hotkey_record": "F10"
    }
