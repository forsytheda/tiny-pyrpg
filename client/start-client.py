# Standard module imports
import ipaddress
import json
import socket
import sys
import threading
from queue import Queue

# PyQt5 imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QErrorMessage

# UI imports
from gui.main_menu import Ui_TPRMainMenu
from gui.lobby_menu import Ui_TPRLobbyMenu
from gui.game_menu import Ui_TPRGameMenu

class MainMenu(QMainWindow):

    def __init__(self, parent):
        super(MainMenu, self).__init__()
        self.parent = parent
        self.ui = Ui_TPRMainMenu()
        self.ui.setupUi(self)
        self.ui.btn_join_game.clicked.connect(self.join_game)

    def join_game(self):
        username = self.ui.txt_username.text()
        ip = self.ui.txt_ip_address.text()
        if len(username) < 4:
            emsg = QErrorMessage(self)
            emsg.setWindowTitle("Tiny-PyRPG: Error")
            emsg.showMessage("Error: username must be at least 4 characters long.")
            return
        if len(username) > 24:
            emsg = QErrorMessage(self)
            emsg.setWindowTitle("Tiny-PyRPG: Error")
            emsg.showMessage("Error: username must not exceed 24 characters long.")
            return
        try:
            ip = ipaddress.IPv4Address(ip)
            ip = str(ip)
            self.parent.connected_ip = ip
            self.parent.username = username
            self.parent.ready = False
            self.parent.command_queue = Queue()
            self.parent.response_queue = Queue()
            t = threading.Thread(target=startClientSocket, args=(self.parent,))
            t.daemon = True
            self.parent.client_socket_thread = t
            t.start()
            self.parent.go_to_lobby()
        except ipaddress.AddressValueError:
            emsg = QErrorMessage(self)
            emsg.setWindowTitle("Tiny-PyRPG: Error")
            emsg.showMessage("Error: IP address invalid. Please use a valid IPv4 address.")
            return

class LobbyMenu(QMainWindow):
    def __init__(self, parent):
        super(LobbyMenu, self).__init__()
        self.parent = parent
        self.ui = Ui_TPRLobbyMenu()
        self.ui.setupUi(self)
        self.ui.lbl_connected_ip.setText(self.parent.connected_ip)

        self.ui.btn_select_cleric.clicked.connect(self.set_prof_cleric)
        self.ui.btn_select_monk.clicked.connect(self.set_prof_monk)
        self.ui.btn_select_paladin.clicked.connect(self.set_prof_paladin)
        self.ui.btn_select_rogue.clicked.connect(self.set_prof_rogue)
        self.ui.btn_select_warrior.clicked.connect(self.set_prof_warrior)
        self.ui.btn_select_wizard.clicked.connect(self.set_prof_wizard)
        self.ui.btn_start.clicked.connect(self.try_start)
        self.ui.btn_ready.clicked.connect(self.set_ready)
        self.ui.btn_exit.clicked.connect(self.exit_lobby)

    def _get_player_labels(self, number):
        labels = {}
        if number == "p1":
            labels["name"] = self.ui.lbl_p1_name
            labels["profession"] = self.ui.lbl_p1_profession
            labels["profession_dsc"] = self.ui.lbl_p1_profession_dsc
            labels["ready"] = self.ui.lbl_p1_ready
        elif number == "p2":
            labels["name"] = self.ui.lbl_p2_name
            labels["profession"] = self.ui.lbl_p2_profession
            labels["profession_dsc"] = self.ui.lbl_p2_profession_dsc
            labels["ready"] = self.ui.lbl_p2_ready
        elif number == "p3":
            labels["name"] = self.ui.lbl_p3_name
            labels["profession"] = self.ui.lbl_p3_profession
            labels["profession_dsc"] = self.ui.lbl_p3_profession_dsc
            labels["ready"] = self.ui.lbl_p3_ready
        elif number == "p4":
            labels["name"] = self.ui.lbl_p4_name
            labels["profession"] = self.ui.lbl_p4_profession
            labels["profession_dsc"] = self.ui.lbl_p4_profession_dsc
            labels["ready"] = self.ui.lbl_p4_ready
        elif number == "p5":
            labels["name"] = self.ui.lbl_p5_name
            labels["profession"] = self.ui.lbl_p5_profession
            labels["profession_dsc"] = self.ui.lbl_p5_profession_dsc
            labels["ready"] = self.ui.lbl_p5_ready
        elif number == "p6":
            labels["name"] = self.ui.lbl_p6_name
            labels["profession"] = self.ui.lbl_p6_profession
            labels["profession_dsc"] = self.ui.lbl_p6_profession_dsc
            labels["ready"] = self.ui.lbl_p6_ready

    def _update_players(self, game):
        lobby = game["lobby"]
        for number, player in lobby.items():
            labels = self._get_player_labels(number)
            labels["name"].setText(player["name"] if not player["name"] == "" else "Empty")
            labels["profession"].setText(player["profession"] if not player["profession"] == "" else "None")
            labels["profession_dsc"].setText(player["profession_dsc"])
            labels["ready"].setText("Yes" if player["ready"] == True else "No")

    def _set_profession(self, prof):
        if self.parent.player["profession"] != prof:
            self.parent.player["profession"] = prof
            self.parent.command_queue.put("UPDATE PROFESSION")

    def set_prof_warrior(self):
        self._set_profession("Warrior")

    def set_prof_rogue(self):
        self._set_profession("Rogue")

    def set_prof_cleric(self):
        self._set_profession("Cleric")

    def set_prof_paladin(self):
        self._set_profession("Paladin")

    def set_prof_monk(self):
        self._set_profession("Monk")

    def set_prof_wizard(self):
        self._set_profession("Wizard")

    def try_start(self):
        self.parent.command_queue.put("TRY START")

    def set_ready(self):
        self.parent.ready = not self.parent.ready
        self.parent.command_queue.put("UPDATE READY")

    def exit_lobby(self):
        self.parent.command_queue.put("EXIT")
        self.parent.client_socket_thread.join()
        self.parent.go_to_main_menu()

class GameMenu(QMainWindow):
    def __init__(self, parent):
        super(GameMenu, self).__init__()
        self.parent = parent
        self.ui = Ui_TPRGameMenu()
        self.ui.setupUi(self)

class ClientSocket:
    def __init__(self, parent):
        print("Creating Socket")
        self.parent = parent
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print("Starting Socket")
        self.sock.connect((self.parent.connected_ip, 52000))
        self.sock.send("Tiny-PyRPG Client".encode())
        data = self.sock.recv(2048)

        if not data or data != "Tiny-PyRPG Server".encode():
            self.sock.shutdown(socket.SHUT_RDWR)()
            self.sock.close()
            emsg = QErrorMessage(self.parent)
            emsg.showMessage("Error: Tried to connect to server. Server failed handshake. Closing connection.")
            self.parent.go_to_main_menu()
            return

        data = {}
        data["request"] = "JOIN LOBBY"
        data["data"] = self.parent.username
        data = json.dumps[data].encode()
        self.sock.sendall(data)

        response = self.sock.recv(2048)
        response = json.loads(response)
        data = response["data"]
        response = response["response"]

        if response == "ERROR":
            if data = "LOBBY FULL":
                emsg = QErrorMessage()
                emsg.setWindowTitle("Tiny-PyRPG | Error: Lobby full")
                emsg.showMessage("Error: the lobby you tried to join is full. Exiting.")
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                self.parent.go_to_main_menu()
                return
            elif data == "NAME TAKEN":
                emsg = QErrorMessage()
                emsg.setWindowTitle("Tiny-PyRPG | Error: Name Taken")
                emsg.showMessage("Error: the lobby you tried to join already has someone with the name you chose. Exiting.")
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                self.parent.go_to_main_menu()
                return
        elif response == "JOIN ACCEPT":
            pnum = data["player-number"]
            lobby = data["lobby"]
            
            
        self.parent.response_queue.put(("UPDATE GAME", game))

        while True:
            command = self.parent.command_queue.get()
            if command == "UPDATE PROFESSION":
                data = {}
                data["request"] = "UPDATE PROFESSION"
                data["data"] = self.parent.player["profession"]
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(2048)
                response = json.loads(response.decode())
                game = response["game"]
                response = response["response"]
                if response != "VALID":
                    emsg = QErrorMessage()
                    emsg.setWindowTitle("Tiny-PyRPG | Error: Command Invalid")
                    emsg.showMessage("Error: the action you just tried to do is broken. Please contact the developer.")
                    continue
                self.parent.window._update_players(game)
                print("Updating profession to {}".format(self.parent.player["profession"]))
            elif command == "UPDATE READY":
                data = {}
                data["request"] = "UPDATE READY"
                data["data"] = self.parent.ready
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(2048)
                response = json.loads(response.decode())
                game = response["game"]
                response = response["response"]
                if response != "VALID":
                    emsg = QErrorMessage()
                    emsg.setWindowTitle("Tiny-PyRPG | Error: Command Invalid")
                    emsg.showMessage("Error: the action you just tried to do is broken. Please contact the developer.")
                    continue
                self.parent.window._update_players(game)
                print("Ready state is now {}".format(self.parent.ready))
            elif command == "TRY START":
                print("Requesting game start")
                data = {}
                data["request"] = "TRY START"
                data["data"] = ""
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(2048)
                response = json.loads(response.decode())
                game = response["game"]
                response = response["response"]
                if response == "START":
                    self.parent.go_to_game()
                    self.parent._update_players(game)
                    print("Game Starting")
                    continue
                elif response == "NOT READY":
                    print("There are players who are not ready.")
                    continue
                else:
                    emsg = QErrorMessage()
                    emsg.setWindowTitle("Tiny-PyRPG | Error: Command Invalid")
                    emsg.showMessage("Error: the action you just tried to do is broken. Please contact the developer.")
                    continue
            elif command == "EXIT":
                data = {}
                data["request"] = "EXIT"
                data["data"] = ""
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                self.sock.shutdown(socket.SHUT_RDWR)(socket.SHUT_RDWR)
                self.sock.close()
                print("Exiting")
                break
            else:
                pass

class Client:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainMenu(self)
        self.window.show()
        self.app.exec_()

    def start_response_queue(self):
        print("Starting response queue")
        while True:
            command, data = self.response_queue.get()
            print("Received command: {}".format(command))
            if command == "UPDATE GAME":
                self.window._update_players(data)
            else:
                print("Unknown command")

    def go_to_main_menu(self):
        self.window.hide()
        del self.window
        self.window = MainMenu(self)
        self.window.show()

    def go_to_lobby(self):
        self.window.hide()
        del self.window
        self.window = LobbyMenu(self)
        self.window.show()

    def go_to_game(self):
        self.window.hide()
        del self.window
        self.window = GameMenu(self)
        self.window.show()

def startClientSocket(client):
    client.socket = ClientSocket(client)
    client.socket.start()

if __name__ == "__main__":
    client = Client()