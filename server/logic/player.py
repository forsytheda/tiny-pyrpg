from .profession import PROFESSION_LIST

class Player:

    def __init__(self, name):
        self.name = name
        self.profession = None
        self.ready = False

    def set_profession(self, profession_name):
        self.profession = PROFESSION_LIST[profession_name]

    def get_profession(self):
        return self.profession
    
    def set_ready(self, ready):
        self.ready = ready

    def to_dict(self):
        player = {}
        player["name"] = self.name
        player["profession"] = self.profession.name
        player["profession_description"] = self.profession.description
        player["ready"] = self.ready
        return player

def get_empty_player_dict():
    p = {}
    p["name"] = ""
    p["profession"] = ""
    p["profession_description"] = ""
    p["ready"] = True
    return p