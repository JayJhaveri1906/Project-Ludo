from utils import roll_dice
import sys
from collections import defaultdict


class Player:
    def __init__(self, pid):
        self.C = pid  # current Player id
        pass


class Pawn:
    def __init__(self, pid, pawnNo, sixReqd):
        self.playerId = pid  # whos pawn is it?
        self.pawnId = pawnNo  # pawn number of that player
        self.pi = -1  # main position (-1: special)
        self.si = 0  # supplemental position (0: start base, 1-5: home stretch, 6: home
        self.sixReqd = sixReqd
        if not self.sixReqd:
            self.pi = 0
            self.si = 0

    def reset(self):  # when killed
        self.pi = -1
        self.si = 0
        if not self.sixReqd:
            self.pi = 0
            self.si = 0


class Board:
    def __init__(self, noOfPlayers, noOfPawnPerPlayer):
        if noOfPlayers > 4 or noOfPawnPerPlayer > 4:
            sys.exit("Now only supports max 4 players max 4 pawns")

        self.boardSize = 52  # 52 board size usually, TODO: may become dynamic later dependent on no of players...

        self.noOfPlayers = noOfPlayers
        self.noOfPPP = noOfPawnPerPlayer  # pawn per player
        self.turn_number = 0
        self.referenceDiff = []

        self.boardDict = defaultdict(set)
        self.safeSpots = set()

        self.finished = defaultdict(int)
        self.homeStretch = False
        self.sixReqd = False

        self.players = []
        pid = 0  # tmp counter
        refDiff = 0  # diff cntr
        for i in range(noOfPlayers):  # Dynamic Game generation
            player = Player(pid)
            self.referenceDiff.append(refDiff)
            pawns = []
            pawnId = 0
            for j in range(noOfPawnPerPlayer):
                pawns.append(Pawn(pid, pawnId, self.sixReqd))  # array of pawn objects for that player
                if not self.sixReqd:
                    gPos = self.getGlobalPos(pid, 0)

                    self.boardDict[gPos].add((pid, pawnId))
                pawnId += 1

            safe_spot = self.getGlobalPos(pid, 0) + 8  # Creates safe pots at startPos + 8 positions
            self.safeSpots.add(safe_spot)

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

        if myPawn.pi == -1:  # special condition

            if not self.homeStretch:
                print("Invalid move brother HOME STRECH is disabled, check your algorithm")
            else:
                if myPawn.si == 0:  # start pos
                    if diceNo == 6:
                        myPawn.pi = 0
                        gPos = self.getGlobalPos(playerChance, myPawn.pi)

                        self.boardDict[gPos].add((myPawn.playerId, myPawn.pawnId))
                    else:
                        print("Can't move out bruh for dice no:", diceNo)
                        # TODO: implement that you cannot select this guy....
                        # not implementing it, decided to use it as a skip turn...
                        # prob don't send them to the algo.
                elif myPawn.si >= 1 or myPawn.si <= 5:  #
                    print("inside home stretch")
                    newSi = myPawn.si + diceNo
                    if (newSi > 6):
                        print("Invalid Move, can't go beyond home")
                    if newSi == 6:
                        print("Reached home bitch")
                        self.finished[myPawn.playerId] += 1
                        if self.finished[myPawn.playerId] == self.noOfPPP:
                            print(myPawn.playerId, "player Won")
                    myPawn.si = newSi

                elif myPawn.si == 6:
                    print("Already Home Bruh, loose chance then")
                    # self.finished[myPawn.playerId] += 1
                    # if self.finished[myPawn.playerId] == self.noOfPPP:
                    #     print(myPawn.playerId, "player Won")

        else:
            newPos = myPawn.pi + diceNo
            if newPos >= self.boardSize:
                # Discard the player from global Dict
                gPos = self.getGlobalPos(playerChance, myPawn.pi)
                self.boardDict[gPos].discard((myPawn.playerId, myPawn.pawnId))

                myPawn.pi = -1  # convert to special cond

                if not self.homeStretch:
                    self.finished[myPawn.playerId] += 1
                else:

                    myPawn.si = newPos - self.boardSize + 1  # Calc pos in homeStretch

                    if myPawn.si == 6:
                        print("reached Home")
                        self.finished[myPawn.playerId] += 1

            else:
                gPos = self.getGlobalPos(playerChance, myPawn.pi)  # get current pos
                self.boardDict[gPos].discard((myPawn.playerId, myPawn.pawnId))  # remove from curr pos

                gPos += diceNo  # get new gPos
                myPawn.pi += diceNo  # update the primary location (all checks done before)

                # Check if safe spot
                if gPos not in self.safeSpots and gPos not in self.referenceDiff:  # if in safeSpots or the initial spawn safe spots, ez add no check
                    # if not safe Spot
                    if len(self.boardDict[gPos]) != 0:  # if collision:

                        for playerId, pawnId in list(self.boardDict[gPos]):
                            if playerId != myPawn.playerId:
                                self.players[playerId][1][pawnId].reset()
                                self.boardDict[gPos].discard((playerId, pawnId))
                                killed = True

                self.boardDict[gPos].add((myPawn.playerId, myPawn.pawnId))

        if killed:
            print("You killed peops bruh jod")

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
        if localPos == -1:
            return localPos
        globalPos = localPos + self.referenceDiff[playerNo]
        return globalPos

    def printState(self, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
        print()
        currPlayer = myPlayer[0]
        currPawns = myPlayer[1]
        print("Current Player Number", currPlayer.C)

        print("_" * 20)

        print("Pawn details:")
        for pawn in currPawns:
            print("Pawn Number", pawn.pawnId)
            print("Local positions", pawn.pi, pawn.si)
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
