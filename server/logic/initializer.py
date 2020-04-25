from .profession import PROFESSION_LIST, Profession
from .action import ACTION_LIST, Action, Modifier, Status

import json
import os

class Initializer:

    def __init__(self):
        self.initialized = False

    def init(self):
        if not self.initialized:
            self.initialized = True
            load_professions_from_json()
            load_actions_from_json()

def load_professions_from_json():
    cwd = os.getcwd()
    base_path = '\\assets\\professions\\'
    full_path = cwd + base_path
    for prof_file in os.listdir(full_path):
        if prof_file.endswith('.json'):
            profession = json.load(open(full_path + prof_file))
            if profession["TPR-Type"] == "profession":
                name = profession["name"]
                description = profession["description"]
                base_attributes = profession["base_attributes"]
                actions = profession["actions"]
                profession = Profession(name, description, base_attributes, actions)
                PROFESSION_LIST[name] = profession
            else:
                raise Exception()
                # TODO: Implement custom load exception
    PROFESSION_LIST["None"] = Profession("None", "Someone who has not chosen a profession", {}, [])

def load_actions_from_json():
    base_path = '\\assets\\actions\\'
    full_path = os.getcwd() + base_path
    for action_file in os.listdir(full_path):
        if action_file.endswith('.json'):
            action = json.load(open(full_path + action_file))
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
                    status_list.append(Status(Modifier(attribute, change), duration, duration_delta))
                ACTION_LIST[name] = Action(name, costs, modifier_list, status_list)
            else:
                raise Exception()
                # TODO: Implement custom load exception