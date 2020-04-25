PROFESSION_LIST = {}

class Profession:

    def __init__(self, name, description, base_attributes, actions):
        self.name = name
        self.description = description
        self.base_attributes = base_attributes
        self.actions = actions

    def to_dict(self):
        d = {}
        d["name"] = self.name
        d["description"] = self.description
        d["base_attributes"] = self.base_attributes
        d["actions"] = self.actions
