import json
from pprint import pprint

def load_config(filepath):
    with open(filepath) as f:
        return json.load(f)

if __name__=="__main__":
    data = load_config("config.json")

    print(data["game_server"]["port"])
    pprint(data)