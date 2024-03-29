from utils import roll_dice
import sys
from collections import defaultdict


class Player:
    def __init__(self, pid):
        self.C = pid  # current Player id
        pass


class Pawn:
    def __init__(self, pid, pawnNo):
        self.playerId = pid  # whos pawn is it?
        self.pawnId = pawnNo  # pawn number of that player
        self.pi = 0

    def reset(self):  # when killed
        self.pi = 0


class Board:
    def __init__(self, noOfPlayers, noOfPawnPerPlayer):
        if noOfPlayers > 4 or noOfPawnPerPlayer > 4:
            sys.exit("Now only supports max 4 players max 4 pawns")

        self.boardSize = 52  # 52 board size usually, TODO: may become dynamic later dependent on no of players...

        self.noOfPlayers = noOfPlayers
        self.noOfPPP = noOfPawnPerPlayer  # pawn per player
        self.turn_number = 0
        self.referenceDiff = []

        self.boardDict = defaultdict(set)  # (plyaerId, pawnId)
        self.safeSpots = set()

        self.finished = defaultdict(int)

        self.players = []
        pid = 0  # tmp counter
        refDiff = 0  # diff cntr
        for i in range(noOfPlayers):  # Dynamic Game generation
            player = Player(pid)
            self.referenceDiff.append(refDiff)
            pawns = []
            pawnId = 0
            for j in range(noOfPawnPerPlayer):
                pawns.append(Pawn(pid, pawnId))  # array of pawn objects for that player
                gPos = self.getGlobalPos(pid, 0)
                self.boardDict[gPos].add((pid, pawnId))
                pawnId += 1

            safe_spot = self.getGlobalPos(pid, 0) + 8  # Creates safe pots at startPos + 8 positions
            self.safeSpots.add(safe_spot)
            self.safeSpots.add(self.getGlobalPos(pid, 0))   # And also at startPos

            self.players.append((player, pawns))  # array of tuple of (playerObject, pawnObjectsArray) datastructure

            pid += 1  # increase pid
            refDiff += 13  # to convert local to global,, TODO: 13 is also yet to be decided to make dynamic??

        print("initialized")
        # we need minimum 4 safe spot and 4 start location even if only 2 players then:
        # TODO: else increase
        #  dynamically,, ,, but we don't support >4 players yet lmfao,, if we do it should work chummi once we figure
        #  out how the game size will increase as the number of players go big. till then 4 player is the default
        #  board size...
        if self.noOfPlayers < 4:
            self.referenceDiff = []
            self.safeSpots = set()
            refDiff = 0
            for pid in range(4):
                self.referenceDiff.append(refDiff)
                refDiff += 13  # TODO: similar to abv

                safe_spot = self.getGlobalPos(pid, 0) + 8  # Creates safe pots at startPos + 8 positions
                self.safeSpots.add(safe_spot)
                self.safeSpots.add(self.getGlobalPos(pid, 0))

    def getNewState(self):
        # Things we need to return,
        playerChance = self.turn_number % self.noOfPlayers  # which player's chance?
        diceNo = roll_dice()  # dice number

        myPlayer = self.players[playerChance]

        return myPlayer, self.boardDict, self.safeSpots, self.referenceDiff, diceNo

    def movePawn(self, pawnNo, diceNo):
        killed = False

        playerChance = self.turn_number % self.noOfPlayers  # which player's chance?

        myPawn = self.players[playerChance][1][pawnNo]  # which pawn did the player select?

        newPos = myPawn.pi + diceNo
        if newPos >= self.boardSize - 1:    # Don't step on the last square anyway
            # Discard the player from global Dict
            gPos = self.getGlobalPos(playerChance, myPawn.pi)
            self.boardDict[gPos].discard((myPawn.playerId, myPawn.pawnId))
            self.finished[myPawn.playerId] += 1
            myPawn.pi = newPos

        else:
            gPos = self.getGlobalPos(playerChance, myPawn.pi)  # get current pos
            self.boardDict[gPos].discard((myPawn.playerId, myPawn.pawnId))  # remove from curr pos

            myPawn.pi += diceNo  # update the primary location (all checks done before)
            gPos = self.getGlobalPos(playerChance, myPawn.pi)  # get new gPos

            # Check if safe spot
            if gPos not in self.safeSpots:  # if in safeSpots or the initial spawn safe spots, ez add no check
                # if not safe Spot
                if len(self.boardDict[gPos]) != 0:  # if collision:
                    for playerId, pawnId in list(self.boardDict[gPos]):
                        if playerId != myPawn.playerId:
                            self.players[playerId][1][pawnId].reset()
                            self.boardDict[gPos].discard((playerId, pawnId))
                            killed = True

            self.boardDict[gPos].add((myPawn.playerId, myPawn.pawnId))

        # if killed:
        #     print("You killed peops bruh jod", myPawn.playerId)

        ## Uncomment if 6 needed to exit
        # if diceNo != 6 and killed == False:
        #     self.turn_number += 1  # proceed to next chance

        if not killed:  # if killed give one more chance!
            self.turn_number += 1

        # Check if win condition
        if self.finished[myPawn.playerId] == self.noOfPPP:
            print(myPawn.playerId, "player Won")
            return myPawn.playerId
        return -1

    def getGlobalPos(self, playerNo, localPos):
        if localPos == -1 or localPos > (self.boardSize - 2):
            return localPos
        globalPos = (localPos + self.referenceDiff[playerNo]) % self.boardSize
        return globalPos


    def getLocalPos(self, playerNo, gpos):
        if gpos > self.boardSize:
            sys.exit("gpos can't be > board size")
        localPos = (gpos - self.referenceDiff[playerNo]) % self.boardSize
        return localPos


    def printState(self, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
        print()
        currPlayer = myPlayer[0]
        currPawns = myPlayer[1]
        print("Current Player Number", currPlayer.C)

        print("_" * 20)

        print("Pawn details:")
        for pawn in currPawns:
            print("Pawn Number", pawn.pawnId)
            print("Local positions", pawn.pi)
            print("Global positions", self.getGlobalPos(pawn.playerId, pawn.pi))
            print("_" * 5)

        print("_" * 20)
        print("Safe Spots")
        print(self.safeSpots)
        print("Spawn Safe Spots")
        print(self.referenceDiff)
        print()
        print("_" * 20)
        print("Global Board")
        print(dict(sorted(boardDict.items())))
        print("_" * 20)
        print("Dice Roll", diceNo)

def humanAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
    p = -1
    while(p not in {0,1,2,3}):
        p = int(input("Enter which pawn do you want to move?"))
        if(p not in {0,1,2,3}):
            print("Enter value between 0 and 3 inclusive")
    return p

if __name__ == "__main__":
    players = int(input("Enter Number of Players: "))
    pawns = int(input("Enter Number of Pawns per Player: "))

    game = Board(players, pawns)
    # game.getNewState()

    while True:
        myPlayer, boardDict, safeSpots, referenceDiff, diceNo = game.getNewState()
        game.printState(myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        p = input("Enter which pawn do you want to move?")
        game.movePawn(int(p), diceNo)
