import json
import os


GOAL_FILE = "goals.json"



def load_goals():

    if not os.path.exists(GOAL_FILE):

        return []


    with open(
        GOAL_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_goals(goals):

    with open(
        GOAL_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            goals,
            f,
            indent=4
        )



def add_goal(goals, text):

    goals.append({

        "task": text,

        "completed": False

    })

    save_goals(goals)



def complete_goal(goals, task):
    
    task = task.lower().strip()


    for goal in goals:

        if goal["task"].lower().strip() == task:

            goal["completed"] = True

            return True


    return False



def get_goals(goals):

    return goals