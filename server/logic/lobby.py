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
            return self.p1
        elif self.p2 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p2 = player
            return self.p2
        elif self.p3 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p3 = player
            return self.p3
        elif self.p4 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p4 = player
            return self.p4
        elif self.p5 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p5 = player
            return self.p5
        elif self.p6 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p6 = player
            return self.p6
        else:
            raise LobbyFullError()

    def remove_player(self, player):
        if self.p1 == player:
            self.p1 == None
            self.names.remove(player.name)
            return self.p1
        elif self.p2 == player:
            self.p2 = None
            self.names.remove(player.name)
            return self.p2
        elif self.p3 == player:
            self.p3 = None
            self.names.remove(player.name)
            return self.p3
        elif self.p4 == player:
            self.p4 = None
            self.names.remove(player.name)
            return self.p4
        elif self.p5 == player:
            self.p5 = None
            self.names.remove(player.name)
            return self.p5
        elif self.p6 == player:
            self.p6 = None
            self.names.remove(player.name)
            return self.p6
        else:
            raise PlayerNotFoundError()

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
        lobby["p1"] = self.p1.to_dict() if self.p1 != None else None
        lobby["p2"] = self.p2.to_dict() if self.p2 != None else None
        lobby["p3"] = self.p3.to_dict() if self.p3 != None else None
        lobby["p4"] = self.p4.to_dict() if self.p4 != None else None
        lobby["p5"] = self.p5.to_dict() if self.p5 != None else None
        lobby["p6"] = self.p6.to_dict() if self.p6 != None else None
        return lobby

class LobbyError(Exception):
    pass

class LobbyFullError(LobbyError):
    pass

class NameTakenError(LobbyError):
    pass

class PlayerNotFoundError(LobbyError):
    pass