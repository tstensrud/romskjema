import os
import json


def iterate_json(data):
    values = []
    for parent_key, nested_dict in data.items():
        parent_key = parent_key.capitalize()
        parent_key = parent_key.replace("_", " ")
        print(parent_key)
        for key, value in nested_dict.items():
            values.append(value)
    return values
    

def load_room_types(data):
    room_types = []
    if isinstance(data, dict):
        room_types = list(data.keys())
    return room_types


json_file_path = os.path.join(os.path.dirname(__file__), "static", f"specifications\skok.json")
with open(json_file_path, encoding="utf-8") as jfile:
    data = json.load(jfile)


pairs = iterate_json(data)
print(pairs)