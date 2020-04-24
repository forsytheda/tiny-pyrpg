import json
import socket
import threading
import time

from logic.game import Game
from logic.lobby import Lobby, LobbyFullError, NameTakenError
from logic.player import Player, get_player

# Starts the listener socket to accept a join clients.
def start_listener(game):
    print("NETWORK: Starting listener.")
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("", 52000))
    listener.listen()
    while True:
        conn, addr = listener.accept()
        print("NETWORK: Connection accepted from: {}.".format(addr))
        data = conn.recv(2048)
        if not data or data != "Tiny-PyRPG Client".encode():
            print("NETWORK: Invalid connection. Shutting down connection from {}.".format(addr))
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            continue
        print("NETWORK: Valid client. Creating new client thread for {}.".format(addr))
        threading._start_new_thread(client_socket, (conn, game))

def client_socket(conn, game):
    conn.sendall("Tiny-PyRPG Server".encode())
    data = json.loads(conn.recv(2048).decode())
    request = data["request"]
    data = data["data"]
    if request != "JOIN LOBBY":
        send_client_error(conn, "INVALID REQUEST")
        return
    username = data
    if game.in_progress == True:
        send_client_error(conn, "GAME STARTED")
        return
    try:
        pnum = game.add_player(Player(username))
    except NameTakenError:
        send_client_error(conn, "NAME TAKEN")
        return
    except LobbyFullError:
        send_client_error(conn, "LOBBY FULL")
        return
    data = {}
    data["response"] = "JOIN ACCEPT"
    jdata = {}
    jdata["player-number"] = pnum
    jdata["lobby"] = game.get_lobby_dict()
    data["data"] = jdata
    data = json.dumps(data).encode()
    conn.sendall(data)
    # The client has now joined the lobby.
    while not game.in_progress:
        data = json.loads(conn.recv(2048).decode())
        request = data["request"]
        data = data["data"]
        if request == "UPDATE PROFESSION":
            profession = data
            if game.update_player_profession(pnum, profession):
                send_client_lobby(conn, game)
                continue
            else:
                send_client_error(conn, "SERVER ERROR")
                return
        elif request == "GET UPDATE":
            send_client_lobby(conn, game)
            continue
        elif request == "UPDATE READY":
            ready = data
            if game.update_player_ready(pnum, ready):
                send_client_lobby(conn, game)
                continue
            else:
                send_client_error(conn, "SERVER ERROR")
                return
        elif request == "TRY START":
            if game.start_game():
                package = {}
                response = "GAME START"
                data = {}
                data["actions"] = game.get_player_profession(pnum).actions()
                data["game"] = game.to_dict()

            else:
                send_client_error(conn, "PLAYERS NOT READY")
                continue


    # The game has now started.
    while game.in_progress:
        pass

def send_client_lobby(conn, game):
    data = {}
    data["response"] = "LOBBY DATA"
    data["data"] = game.get_lobby_dict()
    conn.sendall(json.dumps(data).encode())

def send_client_error(conn, msg):
    data = {}
    data["response"] == "ERROR"
    data["data"] == msg
    data = json.dumps(data).encode()
    conn.sendall(data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def start_server():
    game = Game()
    threading._start_new_thread(start_listener, (game,))

if __name__ == "__main__":
    start_server()