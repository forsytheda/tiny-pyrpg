from copy import deepcopy
from profession import PROFESSION_LIST

class Player:

    def __init__(self, name):
        self.name = name
        self.profession = PROFESSION_LIST["None"]
        self.attributes = None
        self.ready = False

    def set_profession(self, profession):
        self.profession = PROFESSION_LIST[profession]
        self.attributes = deepcopy(self.profession.base_attributes)

    def set_ready(self, ready):
        self.ready = ready

    def lobby_dict(self):
        d = {}
        d["name"] = self.name
        d["profession"] = self.profession.name
        d["profession_description"] = self.profession.description
        d["ready"] = self.ready
        return d

    def game_dict(self):
        d = {}
        d["name"] = self.name
        d["profession"] = self.profession.name
        d["hp"] = [self.attributes["hp"], self.attributes["max_hp"]]
        d["ap"] = [self.attributes["ap"], self.attributes["max_ap"]]
        d["mana"] = [self.attributes["mana"], self.attributes["max_mana"]]
        return d

def get_empty_lobby_dict():
    d = {}
    d["name"] = ""
    d["profession"] = ""
    d["profession_description"] = ""
    d["ready"] = True
    return d

def get_empty_game_dict():
    d = {}
    d["name"] = ""
    d["profession"] = ""
    d["hp"] = [0,0]
    d["ap"] = [0,0]
    d["mana"] = [0,0]
    return d