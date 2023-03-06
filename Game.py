from utils import roll_dice
import sys
from collections import defaultdict


class Player:
    def __init__(self, pid):
        self.C = pid # current Player id
        pass


class Pawn:
    def __init__(self, pid, pawnNo):
        self.playerId = pid  # whos pawn is it?
        self.pawnId = pawnNo  # pawn number of that player
        self.pi = -1  # main position (-1: special)
        self.si = 0  # supplemental position (0: start base, 1-5: home stretch, 6: home

    def reset(self):  # when killed
        self.pi = -1
        self.si = 0


class Board:
    def __init__(self, noOfPlayers, noOfPawnPerPlayer):
        if noOfPlayers > 4 or noOfPawnPerPlayer > 4:
            sys.exit("Now only supports max 4 players max 4 pawns")

        self.boardSize = 52  # 52 board size usually, may become dynamic

        self.noOfPlayers = noOfPlayers
        self.noOfPPP = noOfPawnPerPlayer  # pawn per player
        self.turn_number = 0
        self.referenceDiff = []

        self.boardDict = defaultdict(set)
        self.safeSpots = []  # Will be make dynamically later

        self.finished = defaultdict(int)

        self.players = []
        pid = 0  # tmp counter
        refDiff = 0  # diff cntr
        for i in range(noOfPlayers): # Dynamic Game generation
            player = Player(pid)
            self.referenceDiff.append(refDiff)
            pawns = []
            pawnId = 0
            for j in range(noOfPawnPerPlayer):
                pawns.append(Pawn(pid, pawnId))  # array of pawn objects for that player
                pawnId += 1

            pid += 1
            self.players.append((player, pawns))
            refDiff += 14



    def getNewState(self):
        # Things we need to return,
        playerChance = self.turn_number % self.noOfPlayers  # which player's chance?
        diceNo = roll_dice()  # dice number


        myPlayer = self.players[playerChance]


        return myPlayer, self.boardDict, self.safeSpots, self.referenceDiff, diceNo


    def movePawn(self, pawnNo, diceNo):
        playerChance = self.turn_number % self.noOfPlayers  # which player's chance?


        myPawn = self.players[playerChance][1][pawnNo]



        if myPawn.pi == -1:  # special condition
            if myPawn.si == 0:  # start pos
                if diceNo == 6:
                    myPawn.pi = 0
                    gPos = self.getGlobalPos(playerChance, myPawn.pi)

                    self.boardDict[gPos].add((myPawn.playerId, myPawn.pawnId))
                else:
                    print("Can't move out bruh for dice no:", diceNo)
                    # TODO: implement that you cannot select this guy....
                    # prob don't send them to the algo.
            elif myPawn.si >= 1 or myPawn.si <= 5:  #
                print("inside home stretch")
                # TODO: go home stretch
            elif myPawn.si == 7:
                print("Reached home bitch")
                self.finished[myPawn.playerId] += 1
                if self.finished[myPawn.playerId] == self.noOfPPP:
                    print(myPawn.playerId, "player Won")
                # TODO: go home

        else:
            newPos = myPawn.pi + diceNo
            if newPos >= 52:
                # Discard the player from global Dict
                gPos = self.getGlobalPos(playerChance, myPawn.pi)
                self.boardDict[gPos].discard((myPawn.playerId, myPawn.pawnId))


                myPawn.pi = -1  # convert to special cond

                myPawn.si = newPos - 52 + 1  # Calc pos in homeStretch

                if myPawn.si == 6:
                    print("reached Home")
                    # TODO: something related to reaching home

            else:
                gPos = self.getGlobalPos(playerChance, myPawn.pi)  # get current pos
                self.boardDict[gPos].discard((myPawn.playerId, myPawn.pawnId))  # remove from curr pos

                gPos += diceNo  # get new gPos

                # Check if safe spot
                if gPos not in self.safeSpots: # if in safeSpots ez add no check
                    # if not safe Spot
                    if len(self.boardDict[gPos]) != 0:  # if collision:
                        for playerId, pawnId in self.boardDict[gPos]:
                            if playerId != myPawn.playerId:
                                self.players[playerId][1][pawnId].reset()
                                self.boardDict[gPos].discard((playerId, pawnId))


                self.boardDict[gPos].add((myPawn.playerId, myPawn.pawnId))



        if diceNo != 6:
            self.turn_number += 1  # proceed to next chance


    def getGlobalPos(self, playerNo, localPos):
        globalPos = localPos + self.referenceDiff[playerNo]
        return globalPos

    def movePlayer(self, playerId, pawnId):
        pass

    def printState(self, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
        currPlayer = myPlayer[0]
        currPawns = myPlayer[1]
        print("Current Player", currPlayer.C)

        print("Pawn details:")
        for pawn in currPawns:
            print("Pawn Number", pawn.pawnId)
            print("Local positions", pawn.pi, pawn.si)
            print("Global positions", self.getGlobalPos(pawn.playerId, pawn.pi))


        print("Safe Spots")
        for ss in safeSpots:
            print(ss)

        print("Global Board")
        print(boardDict.items())

        print("Dice Roll", diceNo)


        print("tmp", referenceDiff)








if __name__ == "__main__":
    players = int(input("Enter Number of Players: "))
    pawns = int(input("Enter Number of Pawns per Player: "))

    Game = Board(players, pawns)
    Game.getNewState()

    while True:
        myPlayer, boardDict, safeSpots, referenceDiff, diceNo = Game.getNewState()
        Game.printState(myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        p = input("Enter which pawn do you want to move?")
        Game.movePawn(int(p), diceNo)
