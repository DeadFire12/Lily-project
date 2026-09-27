import json
import os


STATE_FILE = "state.json"


def load_state():

    if not os.path.exists(STATE_FILE):

        return {

            "mood": "happy",

            "activity": "idle",

            "last_action": None

        }


    with open(
        STATE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_state(state):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )



def set_state(state, key, value):

    state[key] = value

    save_state(state)



def get_state(state, key):

    return state.get(key)



def get_all_state(state):

    return state