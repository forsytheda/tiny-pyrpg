PROFESSION_LIST = {}

class Profession:
    
    def __init__(self, name, description, base_attributes, actions):
        self.name = name
        self.description = description
        self.base_attributes = base_attributes
        self.actions = actions

    def to_dict(self):
        p = {}
        p["name"] = self.name
        p["description"] = self.description
        p["base_attributes"] = self.base_attributes
        p["actions"] = self.actions
        return p