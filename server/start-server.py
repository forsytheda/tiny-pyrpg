import json
import socket
import threading

from logic.game import Game
from logic.lobby import Lobby, LobbyFullError, NameTakenError
from logic.player import Player
from logic.action import ACTION_LIST

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
                data["game"] = game.get_game_dict()
                conn.sendall(json.dumps(data).encode())
                break
            else:
                send_client_error(conn, "PLAYERS NOT READY")
                continue
        elif request == "EXIT":
            game.remove_player(pnum)
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            return

    # The game has now started.
    while game.in_progress:
        data = json.loads(conn.recv(2048).decode())
        if not game.in_progress:
            send_client_end_game()
            break
        if not game.is_player_alive(pnum):
            send_client_death(conn)
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            return
        request = data["request"]
        data = data["data"]
        if request == "GET UPDATE":
            send_client_game(conn, game)
            continue
        elif request == "DO ACTION":
            if pnum != game.get_active_player():
                send_client_error(conn, "NOT PLAYER TURN")
                continue
            action = ACTION_LIST[data["action"]]
            source = pnum
            target = data["target"]
            game.do_action(action, source, target)
            send_client_game(conn, game)
            continue
        elif request == "END TURN":
            if pnum != game.get_active_player():
                send_client_error(conn, "NOT PLAYER TURN")
                continue
            game.end_turn()
            send_client_game()
            continue
        else:
            send_client_error("INVALID REQUEST")
            continue


def send_client_lobby(conn, game):
    data = {}
    data["response"] = "LOBBY DATA"
    data["data"] = game.get_lobby_dict()
    conn.sendall(json.dumps(data).encode())

def send_client_game(conn, game):
    data = {}
    data["response"] = "GAME DATA"
    data["data"] = game.get_game_dict()
    conn.sendall(json.dumps(data).encode())

def send_client_end_game(conn, game):
    data = {}
    data["response"] = "END GAME"
    data["data"] = game.get_winner()

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