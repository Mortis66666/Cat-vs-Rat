import json
from .assets import load, BG, ICON
from .enums import direction


with open("settings.json", "r") as file:
    map_name: str = f"maps/{json.load(file)['map']}.json"

del file