# Example Usage:
# ./start_server.py host=192.168.0.100 port=46525
# ./start_server.py host=172.16.54.9
# ./start_server.py port=22645
# ./start_server.py

from .logic.game import Game
from .networking.server_socket import ServerSocket
import sys, ipaddress, os

p_host = None
p_port = None

for arg in sys.argv:
    if arg == sys.argv[0]:
        continue
    if not "=" in arg:
        continue
    parts = arg.split("=")
    if parts[0] == "host":
        try:
            address = ipaddress.IPv4Address(parts[1])
            p_host = str(address)
        except ipaddress.AddressValueError:
            print("ERROR: Provided host argument with invalid IPV4 address.")
            sys.exit(1)
    elif parts[0] == "port":
        try:
            p_port = int(parts[1])
            if p_port <= 0 or p_port >= 65535:
                print("Error: Provided port argument with port outside of valid range.")
                sys.exit(1)
        except ValueError:
            print("ERROR: Provided port argument with invalid port.")
            sys.exit(1)
    else:
        continue

game = Game()
game.start_lobby()

server_socket = ServerSocket(host=("" if p_host==None else p_host), port=(52000 if p_port==None else p_port))
server_socket.start_listening()