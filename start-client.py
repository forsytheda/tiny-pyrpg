import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.main_menu import Ui_TPRMainMenu
from gui.lobby_menu import Ui_TPRLobbyMenu
from gui.game_menu import Ui_TPRGameMenu

class Client:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainMenu()

    def show(self):
        self.window.show()

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
client.show()
sys.exit(client.app.exec())