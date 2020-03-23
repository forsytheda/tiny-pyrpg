class Action:
    def __init__(self, name, mana_cost, ap_cost, modifiers):
        self.name = name
        self.mana_cost = mana_cost
        self.ap_cost = ap_cost
        self.modifiers = modifiers

    def apply(self, source, target):
        if source.attributes["mana"] - self.mana_cost < 0:
            raise ManaError(source, source.attributes["mana"] - self.mana_cost)
        elif source.attribute["ap"] - self.ap_cost < 0:
            pass # Throw ap error
        else:
            for mod in self.modifiers:
                if mod.attribute not in target.attributes:
                    raise ActionError(source, target, mod.attribute)
            for mod in self.modifiers:
                if mod.target_self:
                    source.attributes[mod.attribute] += mod.delta
                else:
                    target.attribute[mod.attribute] += mod.delta
            source.modifers["mana"] -= self.mana_cost
            source.modifers["ap"] -= self.ap_cost

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

class APError(Exception):
    def __init__(self):
        pass