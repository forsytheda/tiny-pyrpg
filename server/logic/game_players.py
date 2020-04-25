from .profession import PROFESSION_LIST
from .action import ACTION_LIST
from threading import Lock

class GamePlayer:
    def __init__(self, player):

        self.isAlive = True

        self.name = player["name"]
        self.profession = PROFESSION_LIST[player["profession"]]

        if self.name != "":
            self.attributes = {}
            base_hp = self.profession.base_attributes["base_hp"]
            self.attributes["hp"] = (base_hp, base_hp)
            base_ap = self.profession.base_attributes["base_ap"]
            self.attributes["ap"] = (base_ap, base_ap)
            base_mana = self.profession.base_attributes["base_mana"]
            self.attributes["mana"] = (base_mana, base_mana)

            self.actions = self.profession.actions

            self.statuses = []

            self.turn_in = 0
        else:
            self.isAlive = False
            self.attributes["hp"] = (0,0)
            self.attributes["ap"] = (0,0)
            self.attributes["mana"] = (0,0)
            self.actions = []
            self.turn_in = 99

    def advance_turn(self, pcount):
        if self.turn_in != 99:
            self.turn_in = self.turn_in % pcount
            for status in self.statuses:
                modifier = status.modifier
                attribute = modifier.attribute
                change = modifier.change
                duration = status.duration
                delta = status.duration_delta
                self.attributes[attribute][0] -= change
                if self.attributes[attribute][0] > self.attributes[attribute][1]:
                    self.attributes[attribute][0] = self.attributes[attribute][1]
                duration -= 1
                change -= duration_delta
                if duration == 0:
                    self.statuses.remove(status)
                    continue
    
    def to_dict(self):
        d = {}
        d["name"] = self.name
        d["profession"] = self.profession.name
        d["hp"] = [self.attributes["hp"][0], self.attributes["hp"][1]]
        d["ap"] = [self.attributes["ap"][0], self.attributes["ap"][1]]
        d["mana"] = [self.attributes["mana"][0], self.attributes["mana"][1]]
        d["turn-in"] = self.turn_in
        return d

class GamePlayers:
    def __init__(self, lobby, pcount):
        self.lock = Lock()
        self.pcount = pcount
        self.active_player = 0
        p1 = lobby["p1"]
        self.p1 = GamePlayer(p1)
        p2 = lobby["p2"]
        self.p2 = GamePlayer(p2)
        p3 = lobby["p3"]
        self.p3 = GamePlayer(p3)
        p4 = lobby["p4"]
        self.p4 = GamePlayer(p4)
        p5 = lobby["p5"]
        self.p5 = GamePlayer(p5)
        p6 = lobby["p6"]
        self.p6 = GamePlayer(p6)

    def advance_turn(self):
        self.lock.acquire()
        self.p1.advance_turn(self.pcount)
        self.p2.advance_turn(self.pcount)
        self.p3.advance_turn(self.pcount)
        self.p4.advance_turn(self.pcount)
        self.p5.advance_turn(self.pcount)
        self.p6.advance_turn(self.pcount)
        self.active_player = ((self.active_player + 1) % self.pcount) if self.active_player + 1 != self.pcount else self.pcount
        self.lock.release()
    
    def get_player_by_number(self, number):
        self.lock.acquire()
        if number == 1: return self.p1
        elif number == 2: return self.p2
        elif number == 3: return self.p3
        elif number == 4: return self.p4
        elif number == 5: return self.p5
        elif number == 6: return self.p6
        self.lock.release()

    def do_action(self, action, source, target):
        self.lock.acquire()
        costs = action.costs
        source.attributes["ap"][0] -= costs["ap"]
        source.attributes["mana"][0] -= costs["mana"]
        for modifier in action.modifier_list:
            attribute = modifier.attribute
            change = modifier.change
            target.attributes[attribute][0] -= change
            if target.attributes[attribute][0] > target.attributes[attribute][1]:
                target.attributes[attribute][0] = target.attributes[attribute][1]
            if target.attributes["hp"][0] <= 0:
                target.isAlive = False
        for status in statuses:
            target.statuses.append(status)
        self.lock.release()

    def get_active_player(self):
        self.lock.acquire()
        pnum = self.active_player
        self.lock.release()
        return pnum

    def game_is_done(self):
        self.lock.acquire()
        players_alive = 0
        if self.p1.isAlive():
            players_alive += 1
        if self.p2.isAlive():
            players_alive += 1
        if self.p3.isAlive():
            players_alive += 1
        if self.p4.isAlive():
            players_alive += 1
        if self.p5.isAlive():
            players_alive += 1
        if self.p6.isAlive():
            players_alive += 1
        if players_alive <= 1:
            return True
        else:
            return False

    def to_dict(self):
        d = {}
        d["p1"] = self.p1.to_dict()
        d["p2"] = self.p2.to_dict()
        d["p3"] = self.p3.to_dict()
        d["p4"] = self.p4.to_dict()
        d["p5"] = self.p5.to_dict()
        d["p6"] = self.p6.to_dict()
        return d
