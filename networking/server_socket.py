import socket, pickle, threading
from ..logic.lobby import LobbyFullError, NameTakenError
from ..logic.player import Player
from .packages.client_package import ClientPackage
from .packages.server_package import ServerPackage

# Definition that will handle all communication with indivual players.
def client_thread(conn, player, game):
    while True:
        data = conn.recv(2048)
        package = (ClientPackage) pickle.loads(data)
        splayer = package.player
        if splayer != player:
            conn.send(pickle.dumps(ServerPackage(game, "INVALID PLAYER")))
            continue
        request = package.request
        if request == "EXECUTE ACTION":
            # TODO: Do action completion
        elif request == "SEND MESSAGE":
            # TODO: Add player message to log
        elif request == "END TURN":
            # TODO: Process end of turn
        else:
            conn.send(pickle.dumps(ServerPackage(game, "INVALID COMMAND")))

# Class that helps coordinate beween threads.
class Lock:
    def __init__(self):
        self.go = True

    def do(self):
        return self.go

    def stop(self):
        self.go = False

# Class that holds the server socket and listens for and accepts incoming connections.
class ServerSocket:

    # Initialized with the host and port to bind to, as well as the game object.
    def __init__(self, host, port, game):
        self.host = host
        self.port = port
        self.game = game
        self.lock = Lock()
        self.create_socket()
        self.start_listening()

    # Basic socket creation with IVP4 TCP
    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
    
    # Listen for, validate, and join players to the game.
    def start_listening(self):
        self.sock.listen(5)
        while self.lock.do():
            conn, addr = self.sock.accept()
            # Make sure we are communicating with a valid client.
            handshake = "TinyPyRPG".encode()
            data = conn.recv(len(handshake))
            if data != handshake:
                conn.shutdown()
                conn.close()
                continue
            # Send confirmation that we are a valid server.
            conn.send(handshake)
            # Receive first ClientPackage.
            data = conn.recv(2048)
            package = (ClientPackage) pickle.loads(data)
            player = package.player
            request = package.request
            # Check to make sure the first request is a join request.
            if request != "JOIN":
                conn.send(ServerPackage(None, "INVALID REQUEST".encode()))
                conn.shutdown()
                conn.close()
                continue
            else:
                # Try to add the player to the game.
                try:
                    # If successfull, return to the player their player number and the current state of the game.
                    pnum = game.add_player(player)
                    player.number = pnum
                    package = ServerPackage(self.game, "JOIN SUCCESSFULL PLAYER NUMBER {}".format(pnum).encode())
                    conn.sendall(pickle.dumps(package))
                    threading._start_new_thread(client_thread, (conn, player, self.game))
                except LobbyFullError:
                    conn.send(ServerPackage(None, "LOBBY FULL".encode()))
                    conn.shutdown()
                    conn.close()
                except NameTakenError:
                    conn.send(ServerPackage(None, "NAME TAKEN".encode()))
                    conn.shutdown()
                    conn.close()
                finally:
                    continue

    def stop_listening():
        self.lock.stop()