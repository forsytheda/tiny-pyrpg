import initializer
from threading import Lock
from player import Player, get_empty_lobby_dict, get_empty_game_dict
from action import ACTION_LIST

class Game:
    
    def __init__(self):
        initializer.init()
        self.in_lobby = True
        self.in_game = False
        self.turn_number = 0
        self.active_player = 0
        self.players = []
        self.lock = Lock()

    def add_player(self, name):
        self.lock.acquire()
        if len(self.players) == 6:
            return -1
        for player in self.players:
            if player.name == name:
                return -2
        player = Player(name)
        self.players.append(player)
        pnum = self.players.index(player)
        self.lock.release()
        return pnum

    def remove_player(self, name):
        self.lock.acquire()
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                self.lock.release()
                return True
        self.lock.release()
        return False

    def get_player_number(self, name):
        self.lock.acquire()
        for player in self.players:
            if player.name == name:
                pnum = self.players.index(player)
                self.lock.release()
                return pnum
        self.lock.release()
        return -1

    def get_player_status(self, name):
        self.lock.acquire()
        pnum = self.get_player_number(name)
        if not self.players[pnum].is_alive:
            return -1
        elif pnum != self.active_player:
            return -2
        else:
            return 0

    def set_player_profession(self, name, profession):
        self.lock.acquire()
        pnum = self.get_player_number(name)
        self.players[pnum].set_profession(profession)
        self.lock.release()

    def set_player_ready(self, name, ready):
        self.lock.acquire()
        pnum = self.get_player_number(name)
        self.players[pnum].set_ready(ready)
        self.lock.release()

    def try_start(self):
        for player in self.players:
            if player.ready == False:
                return False
        self.in_lobby = False
        self.in_game = True
        self.turn_number = 1
        self.active_player = 0
        return True

    def try_action(self, source_name, target_number, action):
        source = self.players[self.get_player_number(source_name)]
        target = self.players[target_number - 1]

        action = ACTION_LIST[action]
        costs = action.costs
        ap_cost = costs["ap"]
        mana_cost = costs["mana"]
        modifiers = action.modifier_list
        statuses = action.status_list

        return 0

    def get_lobby_dict(self):
        d = {}

        if len(self.players) >= 1:
            d["p1"] = self.players[0].lobby_dict()
        else:
            d["p1"] = get_empty_lobby_dict()

        if len(self.players) >= 2:
            d["p2"] = self.players[1].lobby_dict()
        else:
            d["p2"] = get_empty_lobby_dict()

        if len(self.players) >= 3:
            d["p3"] = self.players[2].lobby_dict()
        else:
            d["p3"] = get_empty_lobby_dict()

        if len(self.players) >= 4:
            d["p4"] = self.players[3].lobby_dict()
        else:
            d["p4"] = get_empty_lobby_dict()

        if len(self.players) >= 5:
            d["p5"] = self.players[4].lobby_dict()
        else:
            d["p5"] = get_empty_lobby_dict()

        if len(self.players) >= 6:
            d["p6"] = self.players[5].lobby_dict()
        else:
            d["p6"] = get_empty_lobby_dict()

        return d

    def get_game_dict(self):
        return {}