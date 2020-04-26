""" This module is the starting point of a Tiny-PyRPG Server."""
import json
import socket
import sys
import threading

from game import Game

CLIENT_HANDSHAKE = "Tiny-PyRPG Client".encode()
SERVER_HANDSHAKE = "Tiny-PyRPG Server".encode()

HOST = ""
PORT = 52000

def send_client_error(conn, msg):
    """ Sends the client a specific error message. """
    spkg = {}
    spkg["response"] = "ERROR"
    spkg["data"] = msg
    print(json.dumps(spkg, indent=4))
    spkg = json.dumps(spkg).encode()
    conn.sendall(spkg)

def send_client_lobby(conn, name, game, response="LOBBY DATA"):
    """ Sends the client the current state of the lobby. """
    spkg = {}
    spkg["response"] = response
    data = {}
    pnum = game.get_player_number(name) + 1
    data["player-number"] = pnum
    data["lobby"] = game.get_lobby_dict()
    spkg["data"] = data
    spkg = json.dumps(spkg).encode()
    conn.sendall(spkg)

def send_client_game(conn, name, game, response="GAME DATA"):
    """ Sends the client the current state of the game. """
    spkg = {}
    spkg["response"] = response
    pnum = game.get_player_number(name) + 1
    data = {}
    game_dict = game.get_game_dict()
    game_dict["player-number"] = pnum
    data["actions"] = game.get_player_actions(name)
    data["game"] = game_dict
    spkg["data"] = data
    spkg = json.dumps(spkg).encode()
    conn.sendall(spkg)

def send_client_end_game(conn, won="YOU LOSE"):
    """ Sends the client an end game response. """
    spkg = {}
    spkg["response"] = "END GAME"
    spkg["data"] = won
    spkg = json.dumps(spkg).encode()
    conn.sendall(spkg)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def process_lobby_request(conn, name, game):
    """ This method is used to process requests while in the lobby. """

    

def client_do_action(conn, name, game, data, status):
    """ This method is to break apart the DO ACTION request from
        the main, overloaded game request method. """
    print("{}: is trying to perform the {} action.".format(name, data["action"]))

    # If it is not the player's turn, they cannot do an action.
    if status == -2:
        print("{}: tried to perform an action when it wasn't their turn.".format(name))
        send_client_error(conn, "NOT PLAYER TURN")
    # Otherwise, see what action they want to perform.
    else:
        action = data["action"]
        target = data["target"]
        target = int(target)
        # Try to have them perform the action.
        result = game.try_action(name, target, action)
        # If they don't have enough AP, tell them such.
        if result == -1:
            print("{}: did not have enough AP to perform this action.".format(name))
            send_client_error(conn, "NOT ENOUGH AP")
        # If they don't have enough mana, tell them such.
        elif result == -2:
            print("{}: did not have enough mana to perform this action.".format(name))
            send_client_error(conn, "NOT ENOUGH MANA")
        # Otherwise, they performed the action.
        else:
            print("{}: performed the action.".format(name))
            print("{}: is getting an updated game.".format(name))
            send_client_game(conn, name, game)

def process_game_request(conn, name, game):
    """ This method is used to process a request while in the game. """

    valid_commands = [
        "GET UPDATE",
        "DO ACTION",
        "END TURN"
    ]

    # Listen for the request.
    cpkg = json.loads(conn.recv(4096).decode())

    # If the game has ended not on the client's turn, then they must have lost.
    if not game.in_game:
        print("{}: was in game but the game has ended.")
        send_client_end_game(conn)
        return -1

    request = cpkg["request"]
    data = cpkg["data"]

    # Check the status of the player, and if they died, then they have lost.
    status = game.get_player_status(name)
    print("{}: has the status of {}.".format(name, status))
    if status == -1:
        print("{}: died and is leaving the game.".format(name))
        send_client_end_game(conn)
        return -1

    # If the request is to get an update, send them the game.
    if request == "GET UPDATE":
        print("{}: is getting an updated game.".format(name))
        send_client_game(conn, name, game)

    # If the request is to do an action, try it.
    if request == "DO ACTION":
        client_do_action(conn, name, game, data, status)

    # If the request is to end their turn...
    if request == "END TURN":
        print("{}: is trying to end their turn.".format(name))

        # But is isn't their turn...
        if status == -1:
            # Tell them such.
            print("{}: tried to end their turn when it wasn't their turn.".format(name))
            send_client_error(conn, "NOT PLAYER TURN")

        # Otherwise, end the turn and cycle turns.
        else:
            print("CLIENT: cycling turns.")
            result = game.cycle_turn()
            # If there are multiple clients remaining, update the game.
            if result == 0:
                print("CLIENT: {} is getting an updated game.".format(name))
                send_client_game(conn, name, game)
            # Otherwise the client won and the game ends.
            elif result == -1:
                print("CLIENT: {} won the game!".format(name))
                send_client_end_game(conn, "YOU WIN")
                return -1

    if request not in valid_commands:
        print("CLIENT: {} sent an invalid request.".format(name))
        send_client_error(conn, "INVALID REQUEST")

    return 0

def client_thread(conn, name, game):
    """ This method is designed to run in a separate thread meant to handle
        the connection with a single client instance. """

    print("CLIENT: Starting client threading.Thread for {}.".format(name))
    # Process lobby requests until the game starts.
    while True:
        valid_commands = [
            "EXIT",
            "GET UPDATE",
            "UPDATE PROFESSION",
            "UPDATE READY",
            "TRY START"
        ]

        # To process a request, one must first hear the request.
        cpkg = json.loads(conn.recv(4096).decode())

        # After hearing the request, if the game has started, reply as such and move into the game.
        if game.in_game:
            print("{}: was in lobby when a game was already running.".format(name))
            send_client_game(conn, name, game, "GAME START")
            break

        request = cpkg["request"]
        data = cpkg["data"]

        # If the request was to exit the lobby, remove the player from the lobby and stop talking.
        if request == "EXIT":
            print("{}: is exiting the lobby.".format(name))
            game.remove_player(name)
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            return

        # If the request is to get an update, send the client the lobby.
        if request == "GET UPDATE":
            print("{}: is getting an updated lobby.".format(name))
            send_client_lobby(conn, name, game)

        # If the request is to update the clients profession, do that and send back the lobby.
        if request == "UPDATE PROFESSION":
            print("{}: has updated their profession to {}.".format(name, data))
            game.set_player_profession(name, data)
            print("{}: is getting an updated lobby.".format(name))
            send_client_lobby(conn, name, game)

        # If the request is to update the client's ready state, do that and send back the lobby.
        if request == "UPDATE READY":
            print("{}: has updated their ready state to {}.".format(name, data))
            game.set_player_ready(name, data)
            print("{}: is getting an updated lobby.".format(name))
            send_client_lobby(conn, name, game)

        # If the request is to try and start the game...
        if request == "TRY START":
            print("{}: is trying to start the game.".format(name))
            # Make sure all players are ready...
            if game.try_start():
                # And if the game was started, send the client the game and move to the game.
                print("{}: tried to start the game and all players were ready.".format(name))
                send_client_game(conn, name, game, "GAME START")
                break
            # Otherwise send the client the lobby.
            print("{}: tried to start the game but not all players were ready.".format(name))
            send_client_lobby(conn, name, game)

        # If we don't know what the request is, send the client an error.
        if request not in valid_commands :
            print("{}: sent an invalid request.".format(name))
            send_client_error(conn, "INVALID REQUEST")
        continue

    print("CLIENT: {} has entered the game sequence.".format(name))
    # Process game requests until the game ends.
    while True:
        if process_game_request(conn, name, game) == -1:
            break

def start_listener(game):
    """ This method is designed to be used in a separate thread from the main program.
        It listens for incoming connections and joins players to the game. """

    # First, a socket is created and bound to all interfaces on a specific port.
    print("NETWORK: Starting listener.")
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((HOST, PORT))
    listener.listen(6)

    while game.in_lobby:
        # While the game is in lobby, accept new connections and try to join them to the game.
        conn, addr = listener.accept()
        print("NETWORK: Accepted connection from {}.".format(addr))
        data = conn.recv(4096)
        # If the incoming client does not validate as a Tiny-PyRPG Client, close the connection.
        if data != CLIENT_HANDSHAKE:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            continue
        conn.sendall(SERVER_HANDSHAKE)
        # The client's first request should be to join the lobby.
        cpkg = json.loads(conn.recv(4096).decode())
        request = cpkg["request"]
        data = cpkg["data"]
        # If the client does not, then it is an invalid request and the connection is closed.
        if request != "JOIN LOBBY":
            send_client_error(conn, "INVALID REQUEST")
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            continue
        # If the request is to join the lobby, then the "data" key should lead to their username.
        name = data
        print("NETWORK: Valid client connected as {}.".format(name))
        # We then try to add the player to the game.
        result = game.add_player(name)
        # If the result of this action is -1, then the lobby is full and the connection is closed.
        if result == -1:
            print("ERROR: Client at {} tried to join, but the lobby was full.".format(addr))
            send_client_error(conn, "LOBBY FULL")
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            continue
        # If the result of this action is -2, then someone with that username has already joined
        # and the connection is closed.
        if result == -2:
            print(
                "ERROR: Client at {} tried to join as {}, but the name was already taken."
                .format(addr, name)
            )
            send_client_error(conn, "NAME TAKEN")
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            continue
        # Finally, if there is not error with the action, the player was successfully joined
        # and a client thread is created to handle client-server communication from here.
        print("LOBBY: Player {} joined the lobby from connection {}.".format(name, addr))
        send_client_lobby(conn, name, game, "JOIN ACCEPT")
        c_thread = threading.Thread(target=client_thread, args=(conn, name, game))
        c_thread.daemon = True
        c_thread.start()
        continue

def start_server():
    """ This method creates a game and an accompanying listener. """
    game = Game()
    listening_thread = threading.Thread(target=start_listener, args=(game,))
    listening_thread.daemon = True
    listening_thread.start()
    while True:
        cmd = input("Type EXIT to stop: ")
        if cmd.strip().upper() == "EXIT":
            sys.exit(0)

if __name__ == "__main__":
    start_server()
