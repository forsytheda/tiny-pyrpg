import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from gui.main_menu import Ui_TPRMainMenu
from gui.lobby_menu import Ui_TPRLobbyMenu
from gui.game_menu import Ui_TPRGameMenu
from logic.player import Player

class Client:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = None

    def show(self):
        if not self.window == None:
            self.window.show()

    def load_main_menu(self):
        self.window = MainMenu()
        self.join_game_button = self.window.findChild(QPushButton, 'btn_join_game')
        self.host_game_button = self.window.findChild(QPushButton, 'btn_host_game')
        self.txt_username = self.window.findChild(QLineEdit, 'txt_username')
        self.txt_ip = self.window.findChild(QLineEdit, 'txt_ip_address')

    def load_lobby_menu(self):
        self.window = LobbyMenu()

    def load_game_menu(self):
        self.window = GameMenu()

    def join_game(self):
        if not isinstance(self.window, MainMenu):
            pass
        self.player = Player(-1, self.txt_username.text())

class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.ui = Ui_TPRMainMenu()
        self.ui.setupUi(self)

class LobbyMenu(QMainWindow):
    def __init__(self):
        super(LobbyMenu, self).__init__()
        self.ui = Ui_TPRLobbyMenu()
        self.ui.setupUi(self)

class GameMenu(QMainWindow):
    def __init__(self):
        super(GameMenu, self).__init__()
        self.ui = Ui_TPRGameMenu()
        self.ui.setupUi(self)

client = Client()
client.load_main_menu()
client.show()
sys.exit(client.app.exec())