from threading import Lock
from player import Player, get_empty_lobby_dict, get_empty_game_dict
from action import ACTION_LIST

import initializer

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
        if pnum != self.active_player:
            return -2
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
            if not player.ready:
                return False
        self.in_lobby = False
        self.in_game = True
        self.turn_number = 1
        self.active_player = 0
        return True

    def try_action(self, source_name, target_number, action):
        self.lock.acquire()
        source = self.players[self.get_player_number(source_name)]
        target = self.players[target_number - 1]

        action = ACTION_LIST[action]
        costs = action.costs
        ap_cost = costs["ap"]
        mana_cost = costs["mana"]
        modifiers = action.modifier_list
        statuses = action.status_list

        if source.attributes["ap"] - ap_cost < 0:
            self.lock.release()
            return -1
        if source.attributes["mana"] - mana_cost < 0:
            self.lock.release()
            return -2
        for modifier in modifiers:
            attribute = modifier.attribute
            change = modifier.change
            target[attribute] -= change
        target.statuses.extend(statuses)
        self.lock.release()
        return 0

    def cycle_turn(self):
        self.turn_number += 1
        num_alive = 0
        for player in self.players:
            if player.is_alive:
                num_alive += 1
        if num_alive <= 1:
            return -1
        self.active_player = self.active_player + 1 % len(self.players)
        self.players[self.active_player].process_statuses()

        while not self.players[self.active_player].is_alive:
            self.active_player = self.active_player + 1 % len(self.players)
            self.players[self.active_player].process_statuses()
        num_alive = 0
        for player in self.players:
            if player.is_alive:
                num_alive += 1
        if num_alive <= 1:
            return -1
        return 0

    def get_lobby_dict(self):
        lobby_dict = {}

        if len(self.players) >= 1:
            lobby_dict["p1"] = self.players[0].lobby_dict()
        else:
            lobby_dict["p1"] = get_empty_lobby_dict()

        if len(self.players) >= 2:
            lobby_dict["p2"] = self.players[1].lobby_dict()
        else:
            lobby_dict["p2"] = get_empty_lobby_dict()

        if len(self.players) >= 3:
            lobby_dict["p3"] = self.players[2].lobby_dict()
        else:
            lobby_dict["p3"] = get_empty_lobby_dict()

        if len(self.players) >= 4:
            lobby_dict["p4"] = self.players[3].lobby_dict()
        else:
            lobby_dict["p4"] = get_empty_lobby_dict()

        if len(self.players) >= 5:
            lobby_dict["p5"] = self.players[4].lobby_dict()
        else:
            lobby_dict["p5"] = get_empty_lobby_dict()

        if len(self.players) >= 6:
            lobby_dict["p6"] = self.players[5].lobby_dict()
        else:
            lobby_dict["p6"] = get_empty_lobby_dict()

        return lobby_dict

    def get_game_dict(self):
        game_dict = {}

        if len(self.players) >= 1:
            game_dict["p1"] = self.players[0].lobby_dict()
        else:
            game_dict["p1"] = get_empty_game_dict()

        if len(self.players) >= 2:
            game_dict["p2"] = self.players[1].lobby_dict()
        else:
            game_dict["p2"] = get_empty_game_dict()

        if len(self.players) >= 3:
            game_dict["p3"] = self.players[2].lobby_dict()
        else:
            game_dict["p3"] = get_empty_game_dict()

        if len(self.players) >= 4:
            game_dict["p4"] = self.players[3].lobby_dict()
        else:
            game_dict["p4"] = get_empty_game_dict()

        if len(self.players) >= 5:
            game_dict["p5"] = self.players[4].lobby_dict()
        else:
            game_dict["p5"] = get_empty_game_dict()

        if len(self.players) >= 6:
            game_dict["p6"] = self.players[5].lobby_dict()
        else:
            game_dict["p6"] = get_empty_game_dict()

        return game_dict
