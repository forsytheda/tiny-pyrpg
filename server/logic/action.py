class Action:
    def __init__(self, name, mana_cost, ap_cost, modifiers):
        self.name = name
        self.mana_cost = mana_cost
        self.ap_cost = ap_cost
        self.modifiers = modifiers

class Modifier:
    def __init__(self, attribute, delta, duration=1, duration_delta=0, target_self=False):
        self.attribute = attribute
        self.delta = delta
        self.duration = duration
        self.duration_delta = duration_delta
        self.target_self = target_self

class ActionError(Exception):
    def __init__(self, source, target, attribute):
        self.source = source
        self.target = target
        self.attribute = attribute

    def print_error(self):
        print("ERROR: Action Error | {0} tried to change {1}.attributes[{2}] and failed.".format(self.source.player.name, self.target, self.attribute))
        
class ManaError(Exception):
    def __init__(self, source, delta):
        self.source = source
        self.delta = delta

    def print_error(self):
        print("ERROR: Action Error | {0} tried to use an action using {1} mana but only had {2}.".format(self.source.player.name, self.delta, self.source.attributes["mana"]))

class APError(Exception):
    def __init__(self, source, delta):
        self.source = source
        self.delta = delta

    def print_error(self):
        print("ERROR: Action Error | {0} tried to use an action using {1} AP but only had {2}.".format(self.source.player.name, self.delta, self.source.attributes["ap"]))
        