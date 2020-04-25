PROFESSION_LIST = {}

class Profession:

    def __init__(self, name, description, base_attributes, actions):
        self.name = name
        self.description = description
        self.base_attributes = base_attributes
        self.actions = actions

    def to_dict(self):
        player_dict = {}
        player_dict["name"] = self.name
        player_dict["description"] = self.description
        player_dict["base_attributes"] = self.base_attributes
        player_dict["actions"] = self.actions
        return player_dict
