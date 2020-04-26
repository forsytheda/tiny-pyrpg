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
    data["actions"] = game.get_player_actions(name)
    game_dict = game.get_game_dict()
    game_dict["player-number"] = game.get_player_number(name) + 1
    data["game"] = game_dict
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
    print("CLIENT: Starting client thread for {}.".format(name))
    while True:
        cpkg = loads(conn.recv(4096).decode())
        if game.in_game:
            print("CLIENT: {} was in lobby when a game was already running.".format(name))
            send_client_game(conn, name)
            break
        request = cpkg["request"]
        data = cpkg["data"]
        if request == "GET UPDATE":
            print("CLIENT: {} is getting an updated lobby.".format(name))
            send_client_lobby(conn, name)
        elif request == "UPDATE PROFESSION":
            print("CLIENT: Updating {}'s profession to {}.".format(name, data))
            game.set_player_profession(name, data)
            print("CLIENT: {} is getting an updated lobby.".format(name))
            send_client_lobby(conn, name)
        elif request == "UPDATE READY":
            print("CLIENT: Updating {}'s ready state to {}.".format(name, data))
            game.set_player_ready(name, data)
            print("CLIENT: {} is getting an updated lobby.".format(name))
            send_client_lobby(conn, name)
        elif request == "TRY START":
            print("CLIENT: {} is trying to start the game.".format(name))
            if game.try_start():
                print("CLIENT: all players were ready and {} started the game.".format(name))
                send_client_game(conn, name, "GAME START")
                break
            else:
                print("CLIENT: {} tried to start the game but not all players were ready.".format(name))
                send_client_lobby(conn, name)
        elif request == "EXIT":
            print("CLIENT: {} is exiting the lobby.".format(name))
            game.remove_player(name)
            conn.shutdown(SHUT_RDWR)
            conn.close()
            return
        else:
            print("CLIENT: {} send an invalid request.".format(name))
            send_client_error(conn, "INVALID REQUEST")

    print("CLIENT: {} has entered the game sequence.".format(name))
    while True:
        cpkg = loads(conn.recv(4096).decode())
        if not game.in_game:
            print("CLIENT: {} was in game but the game has ended.")
            send_client_end_game(conn)
            conn.shutdown(SHUT_RDWR)
            conn.close()
            break
        request == cpkg["request"]
        data = cpkg["data"]
        status = game.get_player_status(name)
        if status == -1:
            print("CLIENT: {} is dead and leaving the game.".format(name))
            send_client_end_game(conn, name)
            conn.shutdown(SHUT_RDWR)
            conn.close()
            return
        if request == "GET UPDATE":
            print("CLIENT: {} is getting an updated game.".format(name))
            send_client_game(conn, name)
        elif request == "DO ACTION":
            print("CLIENT: {} is trying to perform the {} action.".format(name, data["action"]))
            if status == -2:
                print("CLIENT: it is not {}'s turn.".format(name))
                send_client_error(conn, "NOT PLAYER TURN")
            else:
                action = data["action"]
                target = data["target"]
                result = game.try_action(name, target, action)
                if result == -1:
                    print("CLIENT: {} did not have enough AP to perform this action.".format(name))
                    send_client_error(conn, "NOT ENOUGH AP")
                elif result == -2:
                    print("CLIENT: {} did not have enough mana to perform this action.".format(name))
                    send_client_error(conn, "NOT ENOUGH MANA")
                else:
                    print("CLIENT: {} performed the action.".format(name))
                    print("CLIENT: {} is getting an updated game.".format(name))
                    send_client_game(conn, name)
        elif request == "END TURN":
            print("CLIENT: {} is trying to end their turn.".format(name))
            if status == -1:
                print("CLIENT: it is not {}'s turn.".format(name))
                send_client_error(conn, "NOT PLAYER TURN")
            else:
                print("CLIENT: cycling turns.")
                result = game.cycle_turn()
                if result == 0:
                    print("CLIENT: {} is getting an updated game.".format(name))
                    send_client_game(conn, name)
                elif result == -1:
                    print("CLIENT: {} won the game!".format(name))
                    send_client_end_game(conn, "YOU WIN")
        else:
            print("CLIENT: {} sent an invalid request.".format(name))
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
