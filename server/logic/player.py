class Player:
    def __init__(self, name):
        self.name = name
        self.profession = None

    def set_profession(self, profession):
        self.profession = profession
        self.profession.player = self