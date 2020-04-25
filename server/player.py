from copy import deepcopy
from profession import PROFESSION_LIST

class Player:

    def __init__(self, name):
        self.name = name
        self.profession = PROFESSION_LIST["None"]
        self.attributes = None
        self.ready = False
        self.statuses = []

    def set_profession(self, profession):
        self.profession = PROFESSION_LIST[profession]
        self.attributes = deepcopy(self.profession.base_attributes)

    def set_ready(self, ready):
        self.ready = ready

    def process_statuses(self):
        for status in self.statuses:
            modifier = status.modifier
            attribute = modifier.attribute
            change = modifier.change
            duration = status.duration
            duration_delta = status.duration_delta
            self.attributes[attribute] -= change
            duration -= 1
            change -= duration_delta
            if change < 0:
                change = 0
            if duration == 0:
                self.statuses.remove(status)

    def lobby_dict(self):
        lobby_dict = {}
        lobby_dict["name"] = self.name
        lobby_dict["profession"] = self.profession.name
        lobby_dict["profession_description"] = self.profession.description
        lobby_dict["ready"] = self.ready
        return lobby_dict

    def game_dict(self):
        game_dict = {}
        game_dict["name"] = self.name
        game_dict["profession"] = self.profession.name
        game_dict["hp"] = [self.attributes["hp"], self.attributes["max_hp"]]
        game_dict["ap"] = [self.attributes["ap"], self.attributes["max_ap"]]
        game_dict["mana"] = [self.attributes["mana"], self.attributes["max_mana"]]
        return game_dict

def get_empty_lobby_dict():
    lobby_dict = {}
    lobby_dict["name"] = ""
    lobby_dict["profession"] = ""
    lobby_dict["profession_description"] = ""
    lobby_dict["ready"] = True
    return lobby_dict

def get_empty_game_dict():
    game_dict = {}
    game_dict["name"] = ""
    game_dict["profession"] = ""
    game_dict["hp"] = [0,0]
    game_dict["ap"] = [0,0]
    game_dict["mana"] = [0,0]
    return game_dict
