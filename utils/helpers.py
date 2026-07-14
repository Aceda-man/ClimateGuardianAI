import json


def load_locations():

    with open(
        "data/nigeria_locations.json",
        "r"
    ) as file:

        return json.load(file)