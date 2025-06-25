import json


def get_next_id(entity: str):
    with open("data/counters.json", "r", encoding="utf-8") as f:
        counters = json.load(f)
    key = f"last_{entity}_id"
    new_id = counters.get(key, 0) + 1
    counters[key] = new_id
    with open("data/counters.json", "r", encoding="utf-8") as f:
        json.dump(counters, f, indent=4)
    return new_id