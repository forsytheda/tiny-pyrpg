from .initializer import Initializer
from .lobby import Lobby
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
        self.in_progress = True

    def add_player(self, player):
        return self.lobby.add_player(player)

    def remove_player(self, player):
        return self.lobby.remove_player(player)

    def all_ready(self):
        return self.lobby.all_ready()

    def run_game(self):
        pass

    def to_dict(self):
        game = {}
        game["lobby"] = self.lobby.to_dict()
        game["in_progress"] = self.in_progress
        game["turn_number"] = self.turn_number
        return game