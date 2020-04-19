PROFESSION_LIST = {}

class Profession:
    def __init__(self, name, description, base_attributes, actions):
        self.name = name
        self.description = description
        self.base_attributes = base_attributes
        self.actions = actions
        