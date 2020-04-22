import json
import socket
import threading
import time

from logic.game import Game
from logic.lobby import Lobby, LobbyFullError, NameTakenError
from logic.player import Player, get_player

ACTIVE_PLAYERS = []

def start_listener(game):
    print("Starting listener.")
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("", 52000))
    listener.listen()
    while True:
        conn, addr = listener.accept()
        print("Connection accepted from: {}.".format(addr))
        data = conn.recv(2048)
        if not data or data != "Tiny-PyRPG Client".encode():
            print("Invalid connection. Shutting down connection.")
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            continue
        print("Valid connection. Creating new client thread.")
        ACTIVE_PLAYERS.append(addr)
        threading._start_new_thread(client_socket, (conn,game))

def client_socket(conn, game):
    conn.sendall("Tiny-PyRPG Server".encode())
    data = conn.recv(2048)
    player = json.loads(data.decode())
    player = get_player(player)
    data = {}
    try:
        game.lobby_lock.acquire()
        player = game.add_player(player)
        game.lobby_lock.release()
    except LobbyFullError:
        data["response"] = "LOBBY FULL"
        data["game"] = None
        data = json.dumps(data)
        conn.sendall(data.encode())
        conn.shutdown(socket.SHUT_RDWR)()
        conn.close()
        return
    except NameTakenError:
        data["response"] = "NAME TAKEN"
        data["game"] = None
        data = json.dumps(data)
        conn.sendall(data.encode())
        conn.shutdown(socket.SHUT_RDWR)()
        conn.close()
        return
    data["response"] = "JOINED GAME"
    data["game"] = game.to_dict()
    data = json.dumps(data)
    conn.sendall(data.encode())
    while True:
        data = conn.recv(2048)
        data = json.loads(data.decode())
        print(data)
        request = data["request"]
        data = data["data"]
        if request == "START":
            if game.all_ready():
                game.in_progress = True
        elif request == "UPDATE READY":
            player.ready = data
        elif request == "END TURN":
            pass
        elif request == "DO ACTION":
            pass
        elif request == "POST MESSAGE":
            pass
        elif request == "EXIT":
            pass
        else:
            pass

def start_server():
    game = Game()
    threading._start_new_thread(start_listener, (game,))
    while not game.in_progress:
        time.sleep(.1)
    game.run_game()

if __name__ == "__main__":
    start_server()