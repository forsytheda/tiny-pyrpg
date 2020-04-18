from .logic.game import Game
from .networking.server_socket import ServerSocket
import sys, ipaddress, os

game = Game()
game.start_lobby()

server_socket = ServerSocket(host="", port=52000)
server_socket.start_listening()