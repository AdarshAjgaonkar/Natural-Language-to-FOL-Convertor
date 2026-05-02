# semantic_map.py

SEMANTIC_MAP = {
    # animals
    "dog": "animal",
    "cat": "animal",
    "lion": "animal",
    "tiger": "animal",
    "horse": "animal",
    "cow": "animal",
    "fish": "animal",
    "bird": "animal",

    # humans
    "teacher": "human",
    "student": "human",
    "doctor": "human",
    "engineer": "human",
    "driver": "human",
    "chef": "human",
    "farmer": "human",
    "child": "human",

    # food
    "meat": "food",
    "rice": "food",
    "milk": "food",

    # objects
    "car": "object",
    "cars": "object",
    "machine": "object",
    "machines": "object",
    "code": "object",
    "programs": "object",
    "data": "object",
    "food": "food"
}

def get_category(word):
    return SEMANTIC_MAP.get(word, word)