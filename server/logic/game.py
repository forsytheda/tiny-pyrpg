from .initializer import Initializer
from .lobby import Lobby
from .game_players import GamePlayers
from queue import Queue
import threading

class Game:

    def __init__(self):
        self.initializer = Initializer()
        self.initializer.init()
        self.lobby = Lobby()
        self.lobby_lock = threading.Lock()
        self.in_progress = False
        self.turn_number = 0

    def start_game(self):
        self.lobby_lock.acquire()
        if self.all_ready():
            self.in_progress = True
            self.game_players = GamePlayers(self.lobby.to_dict(), self.lobby.get_player_count())
            self.lobby_lock.release()
            return True
        else:
            self.lobby_lock.release()
            return False

    def add_player(self, player):
        self.lobby_lock.acquire()
        pnum = self.lobby.add_player(player)
        self.lobby_lock.release()
        return pnum

    def remove_player(self, player):
        self.lobby_lock.acquire()
        pnum = self.lobby.remove_player(player)
        self.lobby_lock.release()
        return pnum

    def update_player_profession(self, number, profession):
        self.lobby_lock.acquire()
        result = self.lobby.update_player_profession(number, profession)
        self.lobby_lock.release()
        return result

    def get_player_profession(self, number):
        self.lobby_lock.acquire()
        profession = self.lobby.get_player_profession(number)
        self.lobby_lock.release()
        return profession

    def update_player_ready(self, number, ready):
        self.lobby_lock.acquire()
        result = self.lobby.update_player_ready(number, ready)
        self.lobby_lock.release()
        return result

    def all_ready(self):
        return self.lobby.all_ready()

    def get_lobby_dict(self):
        self.lobby_lock.acquire()
        l = self.lobby.to_dict()
        self.lobby_lock.release()
        return l

    def to_dict(self):
        self.lobby_lock.acquire()
        game = {}
        game["turn_number"] = self.turn_number
        game["player_number"] = self.player_number
        game["players"] = self.game_players.to_dict()
        self.lobby_lock.release()
        return game