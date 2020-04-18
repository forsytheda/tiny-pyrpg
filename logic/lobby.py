class Lobby:
    
    def __init__(self, ip):
        self.names = []
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.p5 = None
        self.p6 = None
        self.ip = ip

    def add_player(self, player):
        if p1 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p2 = player
            return 1
        elif p2 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p2 = player
            return 2
        elif p3 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p3 = player
            return 3
        elif p4 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p4 = player
            return 4
        elif p5 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p5 = player
            return 5
        elif p6 == None:
            self.check_name(player.name)
            self.names.append(player.name)
            self.p6 = player
            return 6
        else:
            raise LobbyFullError()

    def remove_player(self, player):
        if p1 == player:
            self.p1 == None
            self.names.remove(player.name)
            return 1
        elif p2 == player:
            self.p2 = None
            self.names.remove(player.name)
            return 2
        elif p3 == player:
            self.p3 = None
            self.names.remove(player.name)
            return 3
        elif p4 == player:
            self.p4 = None
            self.names.remove(player.name)
            return 4
        elif p5 == player:
            self.p5 = None
            self.names.remove(player.name)
            return 5
        elif p6 == player:
            self.p6 = None
            self.names.remove(player.name)
            return 6
        else:
            raise PlayerNotFoundError()

    def check_name(self, name):
        if name in self.names:
            raise NameTakenError()

    def get_ip(self):
        return self.ip

class LobbyError(Exception):
    pass

class LobbyFullError(LobbyError):
    pass

class NameTakenError(LobbyError):
    pass

class PlayerNotFoundError(LobbyError):
    pass