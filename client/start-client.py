# Standard module imports
import ipaddress
import json
import socket
import sys
import threading
import time
from queue import Queue

# PyQt5 imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QErrorMessage
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

# UI imports
from gui.main_menu import Ui_TPRMainMenu
from gui.lobby_menu import Ui_TPRLobbyMenu
from gui.game_menu import Ui_TPRGameMenu

########### Main Menu  #####################
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

##################### LOBBY MENU  ##########################
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
        self.ui.btn_refresh.clicked.connect(self.refresh)
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
        return labels

    def _update_players(self, game):
        lobby = game["lobby"]
        for player in lobby.keys():
            labels = self._get_player_labels(player)
            labels["name"].setText(lobby[player]["name"] if not lobby[player]["name"] == "" else "Empty")
            labels["profession"].setText(lobby[player]["profession"] if not lobby[player]["profession"] == "" else "None")
            labels["profession_dsc"].setText(lobby[player]["profession_description"])
            labels["ready"].setText("Yes" if lobby[player]["ready"] == True else "No")
            if lobby[player]["ready"] == True:
                labels["ready"].setStyleSheet('color: green')
            else:
                labels["ready"].setStyleSheet('color: red')

    def _set_profession(self, prof):
        if self.parent.player["profession"] != prof:
            self.parent.player["profession"] = prof
            self.parent.command_queue.put("UPDATE PROFESSION")
    def readonly(self):
        self.ui.btn_start.setEnabled(False)
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
    def refresh(self):
        self.parent.command_queue.put("GET UPDATE")

    def exit_lobby(self):
        self.parent.command_queue.put("EXIT")
        self.parent.client_socket_thread.join()
        self.parent.go_to_main_menu()

#################  GAME MENU  ########################
class GameMenu(QMainWindow):
    def __init__(self, parent):
        super(GameMenu, self).__init__()
        self.parent = parent
        self.ui = Ui_TPRGameMenu()
        self.ui.setupUi(self)
        self.action = {}
        self.target = "P1"
        self.targetNum = 1
        #Button name is odd should be refresh i guess
        self.ui.btn_action_info.clicked.connect(self.refresh)
        self.ui.btn_end_turn.clicked.connect(self.endTurn)
        self.ui.btn_do_selected_action.clicked.connect(self.doAction)
        self.ui.btn_p1_select.clicked.connect(self.p1Select)
        self.ui.btn_p2_select.clicked.connect(self.p2Select)
        self.ui.btn_p3_select.clicked.connect(self.p3Select)
        self.ui.btn_p4_select.clicked.connect(self.p4Select)
        self.ui.btn_p5_select.clicked.connect(self.p5Select)
        self.ui.btn_p6_select.clicked.connect(self.p6Select)
        #self.ui.list_actions.itemClicked.connect(self.actionSelect)


    
    def _get_player_labels(self, number):
        labels = {}
        if number == "p1":
            labels["name"] = self.ui.lbl_p1_name
            labels["profession"] = self.ui.lbl_p1_profession
            labels["hp"] = self.ui.lbl_p1_hp
            labels["ap"] = self.ui.lbl_p1_ap
            labels["mana"] = self.ui.lbl_p1_mana
        elif number == "p2":
            labels["name"] = self.ui.lbl_p2_name
            labels["profession"] = self.ui.lbl_p2_profession
            labels["hp"] = self.ui.lbl_p2_hp
            labels["ap"] = self.ui.lbl_p2_ap
            labels["mana"] = self.ui.lbl_p2_mana
        elif number == "p3":
            labels["name"] = self.ui.lbl_p3_name
            labels["profession"] = self.ui.lbl_p3_profession
            labels["hp"] = self.ui.lbl_p3_hp
            labels["ap"] = self.ui.lbl_p3_ap
            labels["mana"] = self.ui.lbl_p3_mana
        elif number == "p4":
            labels["name"] = self.ui.lbl_p4_name
            labels["profession"] = self.ui.lbl_p4_profession
            labels["hp"] = self.ui.lbl_p4_hp
            labels["ap"] = self.ui.lbl_p4_ap
            labels["mana"] = self.ui.lbl_p4_mana
        elif number == "p5":
            labels["name"] = self.ui.lbl_p5_name
            labels["profession"] = self.ui.lbl_p5_profession
            labels["hp"] = self.ui.lbl_p5_hp
            labels["ap"] = self.ui.lbl_p5_ap
            labels["mana"] = self.ui.lbl_p5_mana
        elif number == "p6":
            labels["name"] = self.ui.lbl_p6_name
            labels["profession"] = self.ui.lbl_p6_profession
            labels["hp"] = self.ui.lbl_p6_hp
            labels["ap"] = self.ui.lbl_p6_ap
            labels["mana"] = self.ui.lbl_p6_mana
        return labels
    
    def _update_players(self, game):
        self.ui.list_actions.clear()
        actions = game["actions"]
        gamedata = game["game"]
        turnnum = gamedata["turn-number"]
        actplayer = gamedata["active-player"]       
        playerdata = gamedata["players"]
        for player in playerdata.keys():
            labels = self._get_player_labels(player)
            labels["name"].setText(playerdata[player]["name"] if not playerdata[player]["name"] == "" else "Empty")
            labels["profession"].setText(playerdata[player]["profession"] if not playerdata[player]["profession"] == "" else "None")
            labels["hp"].setText("{0}/{1}".format(playerdata[player]["hp"][0], playerdata[player]["hp"][1]))
            labels["ap"].setText("{0}/{1}".format(playerdata[player]["ap"][0], playerdata[player]["ap"][1]))
            labels["mana"].setText("{0}/{1}".format(playerdata[player]["mana"][0], playerdata[player]["mana"][1]))
        self.ui.lbl_turn_number.setText(str(turnnum))
        self.ui.lbl_active_player_number.setText(str(actplayer))
        for item in actions:
            self.ui.list_actions.addItem(item)

    def refresh(self):
        self.parent.command_queue.put("GET UPDATE")
    def endTurn(self):
        self.parent.command_queue.put("END TURN")
    def doAction(self):
        selectedAction = self.ui.list_actions.selectedItems()
        if selectedAction ==  []:
            msg = "Select an action"
            self.parent.signal.sig_with_strs.emit(msg)
        else:
            tempAction = str(selectedAction[0].text())
            self.action["action"] = tempAction
            self.action["target"] = self.targetNum
            self.parent.command_queue.put("DO ACTION")
    def p1Select(self):
        self.target = "P1"
        self.targetNum = 1
        self.ui.lbl_selected_target.setText(self.target)
    def p2Select(self):
        self.target = "P2"
        self.targetNum = 2
        self.ui.lbl_selected_target.setText(self.target)
    def p3Select(self):
        self.target = "P3"
        self.targetNum = 3
        self.ui.lbl_selected_target.setText(self.target)
    def p4Select(self):
        self.target = "P4"
        self.targetNum = 4
        self.ui.lbl_selected_target.setText(self.target)
    def p5Select(self):
        self.target = "P5"
        self.targetNum = 5
        self.ui.lbl_selected_target.setText(self.target)
    def p6Select(self):
        self.target = "P6"
        self.targetNum = 6
        self.ui.lbl_selected_target.setText(self.target)
    def actionSelect(self):
        pass


        


class MySignal(QtCore.QObject):
    sig_no_args = QtCore.pyqtSignal()
    sig_with_strs = QtCore.pyqtSignal(str)
    sig_quit = QtCore.pyqtSignal()

#####################################    Start Client Socket    ###################################
class ClientSocket:
    def __init__(self, parent):
        print("Creating Socket")
        self.parent = parent
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print("Starting Socket")
        self.sock.connect((self.parent.connected_ip, 52000))
        self.sock.send("Tiny-PyRPG Client".encode())
        data = self.sock.recv(4096)

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
        data = json.dumps(data).encode()
        self.sock.sendall(data)

        response = self.sock.recv(4096)
        response = json.loads(response)
        data = response["data"]
        response = response["response"] 

        if response == "ERROR":
            if data == "LOBBY FULL":
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
            elif data == "GAME STARTED":
                emsg = QErrorMessage()
                emsg.setWindowTitle("Tiny-PyRPG | Error: Game Started")
                emsg.showMessage("Error: the lobby you tried to join has already begun a match. Exiting.")
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                self.parent.go_to_main_menu()
                return
        elif response == "JOIN ACCEPT":
            pnum = data["player-number"]
            lobby = data["lobby"]
            if pnum == 1:
                self.parent.player = lobby["p1"]
            elif pnum == 2:
                self.parent.player = lobby["p2"]
            elif pnum == 3:
                self.parent.player = lobby["p3"]
            elif pnum == 4:
                self.parent.player = lobby["p4"]
            elif pnum == 5:
                self.parent.player = lobby["p5"]
            elif pnum == 6:
                self.parent.player = lobby["p6"]
                            
        self.parent.command_queue.put("GET UPDATE")


#################################  LOBBY LOOP    #######################################
        while True:
            command = self.parent.command_queue.get()

            ##  Update Profession
            if command == "UPDATE PROFESSION":
                data = {}
                data["request"] = "UPDATE PROFESSION"
                data["data"] = self.parent.player["profession"]
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(4096)
                response = json.loads(response.decode())
                game = response["data"]
                response = response["response"]
                if response == "GAME START":
                    self.parent.signal.sig_no_args.emit()
                    #self.parent.window._update_players(game)
                    print("Game Starting")
                    break
                if response != "LOBBY DATA":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    continue               
                self.parent.window._update_players(game)

            ## Update Ready Status
            elif command == "UPDATE READY":
                data = {}
                data["request"] = "UPDATE READY"
                data["data"] = self.parent.ready
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(4096)
                response = json.loads(response.decode())
                game = response["data"]
                response = response["response"]
                if response == "GAME START":
                    self.parent.signal.sig_no_args.emit()
                    #self.parent.window._update_players(game)
                    print("Game Starting")
                    break
                if response != "LOBBY DATA":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    continue                
                self.parent.window._update_players(game)
                print("Ready state is now {}".format(self.parent.ready))
            
            ## Update Lobby
            elif command == "GET UPDATE":
                data = {}
                data["request"] = "GET UPDATE"
                data["data"] = None
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(4096)
                response = json.loads(response.decode())
                game = response["data"]
                response = response["response"]
                if response == "GAME START":
                    self.parent.signal.sig_no_args.emit()
                    #self.parent.window._update_players(game)
                    print("Game Starting")
                    break
                pn = game["player-number"]
                if int(pn)!= 1:
                    self.parent.window.readonly()
                if response != "LOBBY DATA":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    continue
                self.parent.window._update_players(game)
                print("Lobby Refreshed")
            
            ## Try to start game
            elif command == "TRY START":
                print("Requesting game start")
                data = {}
                data["request"] = "TRY START"
                data["data"] = ""
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(4096)
                response = json.loads(response.decode())
                resp = response["response"]
                game = response["data"]
                if resp == "GAME START":
                    self.parent.signal.sig_no_args.emit()
                    #self.parent.window._update_players(game)
                    print("Game Starting")
                    break
                elif resp == "LOBBY DATA":
                    msg = "Not all players are ready."
                    self.parent.signal.sig_with_strs.emit(msg)
                    print("There are players who are not ready.")
                    continue
                    
                else:
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    continue
            
            #Exit Lobby
            elif command == "EXIT":
                data = {}
                data["request"] = "EXIT"
                data["data"] = ""
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                print("Exiting")
            else:
                pass
        
##################################   Game Loop    #################################
        time.sleep(1)
        self.parent.window._update_players(game)
        while True:
            command = self.parent.command_queue.get()

####################### Do Action  #################
            if command == "DO ACTION":
                target = self.parent.window.target
                #action = self.parent.windown.
                data = {}
                data["request"] = "DO ACTION"
                actionData = self.parent.window.action
                data["data"] = actionData
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(4096)
                response = json.loads(response.decode())
                game = response["data"]
                response = response["response"]
                if response == "END GAME":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    self.parent.signal.sig_quit.emit()
                    break
                elif response == "ERROR":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    continue
                elif response != "GAME DATA":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    continue
                self.parent.window._update_players(game)
                print("Lobby Refreshed")
        
###################### Get Update  #################    
            elif command == "GET UPDATE":
                data = {}
                data["request"] = "GET UPDATE"
                data["data"] = None
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(4096)
                response = json.loads(response.decode())
                game = response["data"]
                response = response["response"]
                if response == "END GAME":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    self.parent.signal.sig_quit.emit()
                    break
                elif response != "GAME DATA":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    continue
                self.parent.window._update_players(game)
                print("Lobby Refreshed")
            
################### End Turn  #######################
            elif command == "END TURN":
                data = {}
                data["request"] = "END TURN"
                data["data"] = None
                data = json.dumps(data).encode()
                self.sock.sendall(data)
                response = self.sock.recv(4096)
                response = json.loads(response.decode())
                game = response["data"]
                response = response["response"]
                if response == "END GAME":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    time.sleep(1)
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    self.parent.signal.sig_quit.emit()
                    break
                elif response != "GAME DATA":
                    msg = game
                    self.parent.signal.sig_with_strs.emit(msg)
                    continue
                self.parent.window._update_players(game)
                print("Turn Ended")



class Client:
    def __init__(self):
        self.signal = MySignal()
        self.signal.sig_no_args.connect(self.go_to_game)
        self.signal.sig_with_strs.connect(self.errorMessage)
        self.signal.sig_quit.connect(self.quit_app)
        self.app = QApplication(sys.argv)
        self.window = MainMenu(self)
        self.window.show()
        self.app.exec_()

    def errorMessage(self, msg):
        emsg = QMessageBox()
        emsg.setWindowTitle("Tiny-PyRPG")
        emsg.setText(msg)
        emsg.exec_()

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
    
    def quit_app(self):
        time.sleep(5)
        self.window.hide()
        del self.window        
        self.app.quit()
        sys.exit()
        

def startClientSocket(client):
    client.socket = ClientSocket(client)
    client.socket.start()

if __name__ == "__main__":
    client = Client()
