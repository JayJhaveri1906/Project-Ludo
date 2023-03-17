from typing import List, Any

from Game import Board
from collections import defaultdict
from Algo_Fast import fastAlgo

def defensiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):

    def oppPawn(pawnobj):
        gpos = game.getGlobalPos(pawnobj.pawnId , pawnobj.pi)
        if (pawnobj.pi) > (game.boardSize - 2):
            return -1

        temp = gpos-1

        while(temp >= 0):
            for pawn in boardDict[temp]:
                if pawn[0] != pawnobj.playerId:
                    break
            temp -= 1
        if temp == -1 :
            temp = game.boardSize - 2
            while(temp > gpos):
                for pawn in boardDict[temp]:
                    if pawnobj.playerId != pawn[0]:
                        break
                temp -= 1
            if temp == gpos:
                return -1
            else:
                return gpos + game.boardSize - 2 -temp
        else:
            return gpos - temp

    def danger_risk(dist):
        return 1/6*(1/2**(dist % 6))

    ## reusing chase
    def calcSafeMove(pawn):
        # gpos = game.getGlobalPos(pawn.playerId, pawn.pi)  # get gPos
        # if (pawn.pi) > (game.boardSize - 2):
        #     return -1

        end_pos_of_pawn = game.boardSize - 2

        cnt = pawn.pi
        while cnt <= end_pos_of_pawn:
            # print(cnt, end=" ")
            gpos = game.getGlobalPos(pawn.playerId, cnt)
            for pawnsPos in boardDict[gpos]:
                pid = pawnsPos[0]
                if pid != pawn.playerId:
                    break
            cnt += 1
        # print("\n")
        if cnt > end_pos_of_pawn:  # didn't find any enemy pawn
            return -1
        else:
            dist = cnt - pawn.pi
            if dist > diceNo:
                return 1
            return -1

    Danger_Piece = defaultdict(list)
    max_val = -float('inf')
    Safe_Piece = []
    pawns = myPlayer[1]

    for pawn in pawns:
        dist = oppPawn(pawn)
        if dist != -1:
            gpos = game.getGlobalPos(pawn.pawnId , pawn.pi)
            if gpos in safeSpots:
                val = pawn.pi / game.boardSize
                Danger_Piece[str(val)].append(pawn.pawnId)
            else:
                val = pawn.pi / game.boardSize + danger_risk(dist)
                Danger_Piece[str(val)].append(pawn.pawnId)
            if val > max_val:
                max_val = val
        canSafelyMove = calcSafeMove(pawn)

        if canSafelyMove != -1 :
            Safe_Piece.append(pawn)
    if len(Danger_Piece[max_val]) >= 1:
        if len(Danger_Piece[max_val]) == 1:
            pawnToMove = Danger_Piece[max_val][0]
        else:
            newPawns = []
            for pawnId in Danger_Piece[max_val]:  # cutshort the pawns array to only store pawns with the max potential
                newPawns.append(pawns[pawnId])

            myNewPlayer = (myPlayer[0], newPawns)
            pawnToMove = fastAlgo(game, myNewPlayer, boardDict, safeSpots, referenceDiff, diceNo)

    elif len(Safe_Piece) >= 1:
        if len(Safe_Piece) == 1:
            pawnToMove = Safe_Piece[0]
        else:
            newPawns = []
            for pawnId in Safe_Piece:  # cutshort the pawns array to only store pawns with the max potential
                newPawns.append(pawns[pawnId])

            myNewPlayer = (myPlayer[0], newPawns)
            pawnToMove = fastAlgo(game, myNewPlayer, boardDict, safeSpots, referenceDiff, diceNo)
    else:
        pawnToMove = fastAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)

    return pawnToMove


if __name__ == "__main__":
    players = int(input("Enter Number of Players: "))
    pawns = int(input("Enter Number of Pawns per Player: "))

    game = Board(players, pawns)

    while True:
        myPlayer, boardDict, safeSpots, referenceDiff, diceNo = game.getNewState()
        """ myPlayer: array of tuple of (playerObject, pawnsObjectArray)
        boardDict: mapping of each global position to a (playerNo, pawnNo) if on it
        safeSpots: set of safe Spots Global positions
        referenceDiff: list of spawn positions which are aso safe Spots
        diceNo: the dice number that came """

        # Game.printState(myPlayer, boardDict, safeSpots, referenceDiff, diceNo)

        p = defensiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        done = game.movePawn(int(p), diceNo)
        if done > -1:
            print("Player", done, "Won")
            break