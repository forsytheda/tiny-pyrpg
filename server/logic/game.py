from .initializer import Initializer
from .lobby import Lobby
from queue import Queue
import threading

class Game:

    def __init__(self):
        self.initializer = Initializer()
        self.initializer.init()
        self.lobby = Lobby()
        self.in_progress = False

    def start_lobby(self):
        if self.in_progress == True: return -1
        joining_players = Queue()
        return 0

    def start_game(self):
        if self.in_progress == True: return -1
        self.in_progress = True
        return 0

    def add_player(self, player):
        num = self.lobby.add_player(player)
        return num

    def remove_player(self, player):
        num = self.lobby.remove_player(player)
        return num
