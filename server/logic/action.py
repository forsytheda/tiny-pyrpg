ACTION_LIST = {}

class Action:
    def __init__(self, name, modifier_list, status_list):
        self.name = name
        self.modifier_list = modifier_list
        self.status_list = status_list

class Modifier:
    def __init__(self, attribute, change):
        self.attribute = attribute
        self.change = change

class Status:
    def __init__(self, modifier, duration = 1, duration_delta = 0):
        self.modifier = modifier
        self.duration = duration
        self.duration_delta = duration_delta