import json
import os


LEARNING_FILE = "learning.json"


# =========================================
# LOAD LEARNING
# =========================================

def load_learning():

    if not os.path.exists(LEARNING_FILE):

        return {}


    try:

        with open(
            LEARNING_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    except Exception as e:

        print(
            "Learning loading error:",
            e
        )

        return {}



# =========================================
# SAVE LEARNING
# =========================================

def save_learning(data):

    with open(
        LEARNING_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )



# =========================================
# LEARN
# =========================================

def learn(data, key, value):

    key = key.lower().strip()

    value = value.strip()


    # Already learned
    if key in data:

        data[key]["value"] = value

        data[key]["times_used"] = (
            data[key].get(
                "times_used",
                0
            ) + 1
        )


        # Increase confidence gradually
        confidence = data[key].get(
            "confidence",
            0
        )


        data[key]["confidence"] = min(
            confidence + 10,
            100
        )


    # New learning
    else:

        data[key] = {

            "value": value,

            "confidence": 50,

            "times_used": 1

        }


    save_learning(
        data
    )



# =========================================
# FIND LEARNING
# =========================================

def find_learning(data, key):

    key = key.lower().strip()

    return data.get(
        key
    )



# =========================================
# GET ALL LEARNING
# =========================================

def get_all_learning(data):

    return data