from json import loads, dumps
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from threading import Thread

from game import Game

CLIENT_HANDSHAKE = "Tiny-PyRPG Client".encode()
SERVER_HANDSHAKE = "Tiny-PyRPG Server".encode()

HOST = ""
PORT = 52000

game = None

def send_client_error(conn, msg):
    spkg = {}
    spkg["response"] = "ERROR"
    spkg["data"] = msg
    spkg = dumps(spkg).encode()
    conn.sendall(spkg)

def send_client_lobby(conn, name, response="LOBBY DATA"):
    global game
    spkg = {}
    spkg["response"] = response
    data = {}
    pnum = game.get_player_number(name) + 1
    data["player-number"] = pnum
    data["lobby"] = game.get_lobby_dict()
    spkg["data"] = data
    spkg = dumps(spkg).encode()
    conn.sendall(spkg)

def send_client_game(conn, name, response="GAME DATA"):
    global game
    spkg = {}
    spkg["response"] = response
    data = {}
    pnum = game.get_player_number(name) + 1
    data["player-number"] = pnum
    data["game"] = game.get_game_dict()
    spkg["data"] = data
    spkg = dumps(spkg).encode()
    conn.sendall(spkg)

def send_client_end_game(conn, won="YOU LOSE"):
    global game
    spkg = {}
    spkg["response"] = "END GAME"
    spkg["data"] = won
    spkg = dumps(spkg).encode()
    conn.sendall(spkg)

def client_thread(conn, name):
    global game

    while game.in_lobby:
        cpkg = loads(conn.recv(4096).decode())
        if game.in_game:
            send_client_error(conn, "GAME STARTED")
            break
        request = cpkg["request"]
        data = cpkg["data"]
        if request == "GET UPDATE":
            send_client_lobby(conn, name)
        elif request == "UPDATE PROFESSION":
            game.set_player_profession(name, data)
            send_client_lobby(conn, name)
        elif request == "UPDATE READY":
            game.set_player_ready(name, data)
            send_client_lobby(conn, name)
        elif request == "TRY START":
            if game.try_start():
                send_client_game(conn, name, "GAME START")
                break
            else:
                send_client_error(conn, "PLAYERS NOT READY")
        elif request == "EXIT":
            game.remove_player(name)
            conn.shutdown(SHUT_RDWR)
            conn.close()
        else:
            send_client_error(conn, "INVALID REQUEST")

    while game.in_game:
        cpkg = loads(conn.recv(4096).decode())
        if not game.in_game:
            break
        request == cpkg["request"]
        data = cpkg["data"]
        status = game.get_player_status(name)
        if status == -1:
            send_client_end_game(conn, name)
            conn.shutdown(SHUT_RDWR)
            conn.close()
            return
        if request == "GET UPDATE":
            send_client_game(conn, name)
        elif request == "DO ACTION":
            if status == -2:
                send_client_error(conn, "NOT PLAYER TURN")
            else:
                action = data["action"]
                target = data["target"]
                result = game.try_action(name, target, action)
                if result == -1:
                    send_client_error(conn, "NOT ENOUGH AP")
                elif result == -2:
                    send_client_error(conn, "NOT ENOUGH MANA")
                else:
                    send_client_game(conn, name)
        elif request == "END TURN":
            if status == -1:
                send_client_error(conn, "NOT PLAYER TURN")
            else:
                result = game.cycle_turn()
                if result == 0:
                    send_client_game(conn, name)
                elif result == -1:
                    send_client_end_game(conn, "YOU WIN")
        else:
            send_client_error(conn, "INVALID REQUEST")  

def start_listener():

    global game

    print("NETWORK: Starting listener.")
    listener = socket(AF_INET, SOCK_STREAM)
    listener.bind((HOST, PORT))
    listener.listen(6)

    while game.in_lobby:
        conn, addr = listener.accept()
        print("NETWORK: Accepted connection from {}.".format(addr))
        data = conn.recv(4096)
        if data != CLIENT_HANDSHAKE:
            conn.shutdown(SHUT_RDWR)
            conn.close()
            continue
        conn.sendall(SERVER_HANDSHAKE)
        cpkg = loads(conn.recv(4096).decode())
        request = cpkg["request"]
        data = cpkg["data"]
        if request != "JOIN LOBBY":
            send_client_error(conn, "INVALID REQUEST")
            conn.shutdown(SHUT_RDWR)
            conn.close()
            continue
        name = data
        print("NETWORK: Valid client connected as {}.".format(name))
        result = game.add_player(name)
        if result == -1:
            print("ERROR: Client at {} tried to join, but the lobby was full.".format(addr))
            send_client_error(conn, "LOBBY FULL")
            conn.shutdown(SHUT_RDWR)
            conn.close()
            continue
        elif result == -2:
            print(
                "ERROR: Client at {} tried to join as {}, but the name was already taken."
                .format(addr, name)
            )
            send_client_error(conn, "NAME TAKEN")
            conn.shutdown(SHUT_RDWR)
            conn.close()
            continue
        else:
            print("LOBBY: Player {} joined the lobby from connection {}.".format(name, addr))
            send_client_lobby(conn, name, "JOIN ACCEPT")
            c_thread = Thread(target=client_thread, args=(conn, name))
            c_thread.start()
            continue

def start_server():
    global game
    if game is not None:
        return
    game = Game()
    start_listener()

if __name__ == "__main__":
    start_server()
