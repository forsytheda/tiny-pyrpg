from .player import get_empty_player_dict

class Lobby:
    
    def __init__(self):
        self.names = []
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.p5 = None
        self.p6 = None

    def add_player(self, player):
        if self.p1 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p1 = player
            return 1
        elif self.p2 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p2 = player
            return 2
        elif self.p3 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p3 = player
            return 3
        elif self.p4 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p4 = player
            return 4
        elif self.p5 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p5 = player
            return 5
        elif self.p6 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p6 = player
            return 6
        else:
            raise LobbyFullError()

    def remove_player(self, pnum):
        if pnum == 1:
            self.p1 == None
            self.names.remove(player.name)
            return 1
        elif pnum == 2:
            self.p2 = None
            self.names.remove(player.name)
            return 2
        elif pnum == 3:
            self.p3 = None
            self.names.remove(player.name)
            return 3
        elif pnum == 4:
            self.p4 = None
            self.names.remove(player.name)
            return 4
        elif pnum == 5:
            self.p5 = None
            self.names.remove(player.name)
            return 5
        elif pnum == 6:
            self.p6 = None
            self.names.remove(player.name)
            return 6

    def check_name(self, name):
        if name in self.names:
            raise NameTakenError()

    def all_ready(self):
        num_players = 0
        ready = True
        if self.p1 != None:
            num_players += 1
            ready = self.p1.ready
        if self.p2 != None:
            num_players += 1
            ready = self.p2.ready
        if self.p3 != None:
            num_players += 1
            ready = self.p3.ready
        if self.p4 != None:
            num_players += 1
            ready = self.p4.ready
        if self.p5 != None:
            num_players += 1
            ready = self.p5.ready
        if self.p6 != None:
            num_players += 1
            ready = self.p6.ready
        if num_players % 2 != 0:
            ready = False
        return ready

    def to_dict(self):
        lobby = {}
        lobby["p1"] = self.p1.to_dict() if self.p1 != None else get_empty_player_dict()
        lobby["p2"] = self.p2.to_dict() if self.p2 != None else get_empty_player_dict()
        lobby["p3"] = self.p3.to_dict() if self.p3 != None else get_empty_player_dict()
        lobby["p4"] = self.p4.to_dict() if self.p4 != None else get_empty_player_dict()
        lobby["p5"] = self.p5.to_dict() if self.p5 != None else get_empty_player_dict()
        lobby["p6"] = self.p6.to_dict() if self.p6 != None else get_empty_player_dict()
        return lobby

    def get_player_count(self):
        num_players = 0
        if self.p1 != None:
            num_players += 1
        if self.p2 != None:
            num_players += 1
        if self.p3 != None:
            num_players += 1
        if self.p4 != None:
            num_players += 1
        if self.p5 != None:
            num_players += 1
        if self.p6 != None:
            num_players += 1
            return num_players

    def update_player_profession(self, number, profession):
        if number == 1:
            self.p1.set_profession(profession)
            return True
        elif number == 2:
            self.p2.set_profession(profession)
            return True
        elif number == 3:
            self.p3.set_profession(profession)
            return True
        elif number == 4:
            self.p4.set_profession(profession)
            return True
        elif number == 5:
            self.p5.set_profession(profession)
            return True
        elif number == 6:
            self.p6.set_profession(profession)
            return True
        else:
            return False

    def update_player_ready(self, number, ready):
        if number == 1:
            self.p1.set_ready(ready)
            return True
        elif number == 2:
            self.p2.set_ready(ready)
            return True
        elif number == 3:
            self.p3.set_ready(ready)
            return True
        elif number == 4:
            self.p4.set_ready(ready)
            return True
        elif number == 5:
            self.p5.set_ready(ready)
            return True
        elif number == 6:
            self.p6.set_ready(ready)
            return True
        else:
            return False

    def get_player_profession(self, number):
        if number == 1:
            return self.p1.get_profession()
        elif number == 2:
            return self.p2.get_profession()
        elif number == 3:
            return self.p3.get_profession()
        elif number == 4:
            return self.p4.get_profession()
        elif number == 5:
            return self.p5.get_profession()
        elif number == 6:
            return self.p6.get_profession()
        else:
            return None

class LobbyError(Exception):
    pass

class LobbyFullError(LobbyError):
    pass

class NameTakenError(LobbyError):
    pass