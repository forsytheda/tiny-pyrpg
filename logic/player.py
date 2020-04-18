from .profession import PROFESSION_LIST
import json

class Player:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.profession = None
        self.ready = False

    def set_profession(self, profession_name):
        self.profession = PROFESSION_LIST[profession_name]
