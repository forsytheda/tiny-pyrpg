import random
from action import Action, Modifier

class Profession:
    def __init__(self):
        self.player = None
        self.attributes = {}
        # HP represents the life of a character. When a character's HP reaches 0, the character
        # dies. HP is regained either when the character uses the rest action, or when healed 
        # by another character's special action.
        self.attributes["hp"] = 0
        self.attributes["max_hp"] = 0

        # Mana represents the spirit of a character. Special actions all uses mana as a cost
        # for their use. Mana is regained by a set amount at the start of every turn.
        self.attributes["mana"] = 0
        self.attributes["max_mana"] = 0

        # AP represents the character's ability to take actions on a given turn. Taking any action
        # uses AP, and it returns to full at the start of every turn, unless the character
        # has temp AP which is applied at the beginning of the turn and set to 0 at the end.
        self.attributes["ap"] = 5
        self.attributes["max_ap"] = 5

        # Action offsets represent a character's innate proficience in a given action. The attack
        # offset means that a character hits harder, the defense offset means a character takes less
        # damage from a hit, the endurance offset reduces the cost of special actions, and the
        # heal offset boosts the health gained through healing actions.
        # Attack represents how much damage an action deals to a target.
        # Defense represents how much damage is negated from an incoming attack.
        self.attributes["attack_offset"] = 0
        self.attributes["defense_offset"] = 0
        self.attributes["endurance_offset"] = 0
        self.attributes["heal_offset"] = 0

        # Stat offsets represent a character's physical characteristics. The health offset affects
        # the character's starting max health while the mana offset does the same with mana. These
        # only affect starting characters and play no role on character progression.
        self.attributes["health_offset"] = 0
        self.attributes["mana_offset"] = 0
        #
        # Temporary stats represent changes in a stat for a given time. Temp HP will be depleted
        # before a character starts to lose their normal HP. Temp attack and temp defense
        # represent a temporary boost to either the attack or defend action and will be lost
        # at the end of the turn. The same is temp AP, except it is added to AP at the beginning
        # of the turn and immediately reset to zero.
        self.attributes["temp_hp"] = 0
        self.attributes["temp_attack"] = 0
        self.attributes["temp_defense"] = 0
        self.attributes["temp_ap"] = 0

        # TBD
        self.actions = {}

        self.actions["attack"] = Action("Basic Attack", 0, 3, [Modifier("hp", -(random.randint(0, 10) + self.attributes["attack_offset"]))])
    
    # Stores the player that owns this profession instance
    def set_player(self, player):
        if self.player == None:
            self.player = player

    # Initializes stats to their correct base values based on stat offsets.
    def init_stats(self):
        self.attributes["hp"] = self.attributes["max_hp"] = 100 + self.attributes["health_offset"]
        self.attributes["mana"] = self.attributes["max_mana"] = 50 + self.attributes["mana_offset"]

class Fighter(Profession):
    def __init__(self):
        super().__init__()

        self.attributes["attack_offset"] = 2
        self.attributes["defense_offset"] = 1
        self.attributes["health_offset"] = 20
        self.init_stats()

        self.actions["protect"] = Action("Protect", 0, 2, [Modifier("defense_offset", random.randint(1, 5) + self.attributes["defense_offset"], 1)])

class Rogue(Profession):
    def __init__(self):
        super().__init__()

        self.attributes["attack_offset"] = 3
        self.attributes["heal_offset"] = -5
        self.attributes["mana_offset"] = 25
        self.init_stats()

        self.actions["sneak"] = Action("Sneak", 0, 2, [Modifier("defense_offset", 10, 5, 0, True)])

class Cleric(Profession):
    def __init__(self):
        super().__init__()

        self.attributes["defense_offset"] = 1
        self.attributes["heal_offset"] = 2
        self.attributes["mana_offset"] = 10
        self.init_stats()

        self.actions["heal"] = Action("Basic Heal", 5, 3, [Modifier("hp", -(random.randint(1,5) + self.attributes["heal_offset"]))])

class Wizard(Profession):
    def __init__(self):
        super().__init__()
        self.attributes["attack_offest"] = 5
        self.attributes["defense_offset"] = -5
        self.attributes["mana_offset"] = 50
        self.attributes["health_offset"] = -20
        self.init_stats()

        self.actions["fireball"] = Action("Fireball", 5, 3, [Modifier("hp", random.randint(4, 10) + self.attributes["attack_offset"])])