# Standard module imports
import ipaddress
import socket
import sys
import threading

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
            threading._start_new_thread(StartClientSocket, (self.parent, ip))
            self.parent.connected_ip = ip
            self.parent.go_to_lobby()
        except ipaddress.AddressValueError:
            emsg = QErrorMessage(self)
            emsg.setWindowTitle("Tiny-PyRPG: Error")
            emsg.showMessage("Error: IP address invalid. Please use a valid IPv4 address.")
            return

class LobbyMenu(QMainWindow):
    def __init__(self, parent, ip):
        super(LobbyMenu, self).__init__()
        self.parent = parent
        self.ui = Ui_TPRLobbyMenu()
        self.ui.setupUi(self)
        self.ui.lbl_connected_ip.setText(ip)

class GameMenu(QMainWindow):
    def __init__(self, parent):
        super(GameMenu, self).__init__()
        self.parent = parent
        self.ui = Ui_TPRGameMenu()
        self.ui.setupUi(self)

class ClientSocket:
    def __init__(self, parent):
        self.parent = parent
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.sock.connect((self.parent.connected_ip, 52000))
        self.sock.send("Tiny-PyRPG Client".encode())
        data = self.sock.recv(2048)
        if not data or data != "Tiny-PyRPG Server".encode():
            self.sock.shutdown()
            self.sock.close()
            emsg = QErrorMessage(self.parent)
            emsg.showMessage("Error: Tried to connect to server. Server failed handshake. Closing connection.")
            self.parent.go_to_main_menu()
            return
        # Create player object
        # Send starting info to server
        # Handle joining and passing info to lobby menu
        # While loop for handling client-server communication

class Client:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainMenu(self)
        self.window.show()
        self.app.exec_()

    def go_to_main_menu(self):
        self.window.hide()
        del self.window
        self.window = MainMenu(self)
        self.window.show()

    def go_to_lobby(self):
        self.window.hide()
        del self.window
        self.window = LobbyMenu(self, self.connected_ip)
        self.window.show()

    def go_to_game(self):
        self.window.hide()
        del self.window
        self.window = GameMenu(self)
        self.window.show()

def StartClientSocket(client, ip):
    client.socket = ClientSocket(client)
    client.socket.start()

if __name__ == "__main__":
    client = Client()