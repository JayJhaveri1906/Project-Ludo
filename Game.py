from utils import roll_dice

class Player:
    def __init__(self, pid):
        self.C = pid # current Player id
        pass


class Pawn:
    def __init__(self, pid, pawnNo):
        self.playerId = pid  # whos pawn is it?
        self.pawnId = pawnNo  # pawn number of that player
        self.pi = 0  # main position (0: special)
        self.si = 1  # supplemental position (1: start base, 2-6: home stretch, 7: home

    def reset(self):  # when killed
        self.pi = 0
        self.si = 0


class Board:
    def __init__(self, noOfPlayers, noOfPawnPerPlayer):
        players = []
        pid = 0  # tmp counter
        for i in range(noOfPlayers):
            player = Player(pid)
            pawns = []
            pawnId = 0
            for j in range(noOfPawnPerPlayer):
                pawns.append(Pawn(pid, pawnId))
                pawnId += 1

            pid += 1
            players.append((player, pawns))

        print(players)


