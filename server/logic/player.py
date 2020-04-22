from .profession import PROFESSION_LIST

class Player:

    def __init__(self, name):
        self.name = name
        self.profession = None
        self.ready = False

    def set_profession(self, profession_name):
        if profession_name == "":
            return
        self.profession = PROFESSION_LIST[profession_name]
    
    def set_ready(self, ready):
        self.ready = ready

    def to_dict(self):
        player = {}
        player["name"] = self.name
        player["profession"] = self.profession.name
        player["profession_dsc"] = self.profession.description
        player["ready"] = self.ready
        return player


def get_player(json):
    name = json["name"]
    profession = json["profession"]
    ready = json["ready"]
    player = Player(name)
    player.set_profession(profession)
    player.set_ready(ready)
    return player