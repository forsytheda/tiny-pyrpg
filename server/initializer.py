from json import load
from os import getcwd, listdir

from action import ACTION_LIST, Action, Modifier, Status
from profession import PROFESSION_LIST, Profession

PROFESSION_BASE_PATH = "\\assets\\professions\\"
ACTION_BASE_PATH = "\\assets\\actions\\"

def init():
    PROFESSION_LIST.clear()
    ACTION_LIST.clear()
    cwd = getcwd()
    prof_path = cwd + PROFESSION_BASE_PATH
    for prof_file in listdir(prof_path):
        if prof_file.endswith('.json'):
            profession = load(open(prof_path + prof_file))
            if profession["TPR-Type"] == "profession":
                name = profession["name"]
                description = profession["description"]
                base_attributes = profession["base_attributes"]
                actions = profession["actions"]
                profession = Profession(name, description, base_attributes, actions)
                PROFESSION_LIST[name] = profession
    PROFESSION_LIST["None"] = Profession("None", "Someone who has not chosen a profession", {}, [])
    action_path = cwd + ACTION_BASE_PATH
    for action_file in listdir(action_path):
        if action_file.endswith('.json'):
            action = load(open(action_path + action_file))
            if action["TPR-Type"] == "action":
                name = action["name"]
                costs = action["costs"]
                modifier_list = []
                for modifier in action["modifiers"]:
                    attribute = modifier["attribute"]
                    change = modifier["change"]
                    modifier_list.append(Modifier(attribute, change))
                status_list = []
                for status in action["statuses"]:
                    modifier = status["modifier"]
                    attribute = modifier["attribute"]
                    change = modifier["change"]
                    duration = status["duration"]
                    duration_delta = status["duration_delta"]
                    status_list.append(
                        Status(Modifier(attribute, change), duration, duration_delta)
                    )
                ACTION_LIST[name] = Action(name, costs, modifier_list, status_list)
