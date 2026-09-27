import json
import os
from datetime import datetime


MEMORY_FILE = "memory.json"


# =========================================
# TIME
# =========================================

def now():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



# =========================================
# CATEGORY DETECTION
# =========================================

def detect_category(key):

    key = key.lower().strip()


    if key.startswith("favorite"):

        return "preferences"


    if key.startswith("explanation"):

        return "preferences"


    if key.startswith("like"):

        return "likes"


    if key.startswith("dislike"):

        return "history"


    if key.startswith("used to like"):

        return "history"


    if key in [

        "name",
        "age",
        "birthday",
        "location"

    ]:

        return "personal"


    return "general"



# =========================================
# IMPORTANCE
# =========================================

def detect_importance(key):

    key = key.lower()


    important = [

        "name",
        "birthday",
        "location",
        "favorite game",
        "favorite color"

    ]


    if key in important:

        return "high"


    return "normal"



# =========================================
# LOAD MEMORY
# =========================================

def load_memory():

    if not os.path.exists(MEMORY_FILE):

        return {}


    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)



        upgraded = {}


        for key, value in data.items():


            if isinstance(value, dict):

                upgraded[key] = value


            else:

                upgraded[key] = {

                    "value": str(value),

                    "created": now(),

                    "updated": now(),

                    "category": detect_category(key),

                    "confirmed": True,

                    "confidence": 100,

                    "importance": detect_importance(key)

                }


        return upgraded


    except Exception as e:

        print(
            "Memory loading error:",
            e
        )

        return {}



# =========================================
# SAVE MEMORY
# =========================================

def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(

            memory,

            file,

            indent=4,

            ensure_ascii=False,

            sort_keys=True

        )



# =========================================
# NORMALIZE KEY
# =========================================

def normalize_key(key):

    return key.lower().strip()



# =========================================
# REMEMBER
# =========================================

def remember(memory, key, value):

    key = normalize_key(key)

    value = value.strip()

    current = now()



    if key in memory:


        old_value = memory[key].get(
            "value",
            ""
        )


        if old_value.lower() == value.lower():

            return



        created = memory[key].get(
            "created",
            current
        )


    else:

        created = current



    memory[key] = {


        "value": value,


        "created": created,


        "updated": current,


        "category":
            detect_category(key),


        "confirmed":
            True,


        "confidence":
            100,


        "importance":
            detect_importance(key)

    }



    save_memory(memory)



# =========================================
# FIND MEMORY
# =========================================

def find_memory(memory, key):

    key = normalize_key(key)

    return memory.get(key)



# =========================================
# DELETE MEMORY
# =========================================

def forget_memory(memory, key):

    key = normalize_key(key)


    if key in memory:

        del memory[key]

        save_memory(memory)

        return True


    return False



# =========================================
# DELETE ALL
# =========================================

def forget_all(memory):

    memory.clear()

    save_memory(memory)



# =========================================
# CATEGORY SEARCH
# =========================================

def get_memories_by_category(memory, category):

    results = {}


    for key, data in memory.items():

        if data.get("category") == category:

            results[key] = data



    return results



# =========================================
# ALL CATEGORIES
# =========================================

def get_all_categories(memory):

    categories = set()


    for data in memory.values():

        categories.add(

            data.get(
                "category",
                "general"
            )

        )


    return list(categories)