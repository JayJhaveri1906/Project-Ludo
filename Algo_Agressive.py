from Game import Board
from Algo_Fast import fastAlgo
from collections import defaultdict
import time


def agressiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
    # My Priority in Agressiveness
    ##  1) If instant kill, then kill
    ##      a) Have weighted kills (smart aggressive) cancel here
    ##  2) else: move the one that is closest to enemey
    ##      a) Here to it should be weighted as in I should prioritze the enemey which is closer to its home

    # NOTE: Only looking one step into the future currently
    pawnToMove = -1  # Final pawn to move


    # Calculates kill potential
    def calcKillMetric(pawn):
        if pawn.pi > (game.boardSize - 2):  # removes in active pawns
            return -1

        gpos = game.getGlobalPos(pawn.playerId, pawn.pi+diceNo)  # get new position in gPos

        end_pos_of_pawn = game.getGlobalPos(pawn.playerId, 50)

        # if gposCurr < end_pos_of_pawn and gpos > end_pos_of_pawn: # finishes the game
        #     return -1
        if (pawn.pi + diceNo) > (game.boardSize - 2):
            return -1

        enemy_count = 0
        if gpos not in safeSpots and gpos not in referenceDiff:  # Check if not on safe spot
            for pawnsPos in boardDict[gpos]:
                pid = pawnsPos[0]
                if pid != pawn.playerId:
                    enemy_count += 1  # count how many enemey players you can kill

        return enemy_count

    # Calculates chase potential
    # Chase metric: find first opp pawn, if dist > diceroll, then a chase is possible
    def calcChaseMetric(pawn):
        # gpos = game.getGlobalPos(pawn.playerId, pawn.pi)  # get gPos


        # end_pos_of_pawn = game.getGlobalPos(pawn.playerId, 50)
        end_pos_of_pawn = game.boardSize - 2
        # print("pid, pawnId, pi", pawn.playerId, pawn.pawnId, pawn.pi)
        # print("gpos, endpos", gpos, end_pos_of_pawn)

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


    player = myPlayer[0]  # Extracting player
    pawns = myPlayer[1]  # Extracting the pawns

    playablePawns = defaultdict(list)  # dictionary to store pawn id wrt their potentials
    maxPotential = -1  # max potential to have O(1) access to the max potential pawn

    # Step 1: Checking Instant Kill
    for pawn in pawns:
        potential = calcKillMetric(pawn)  # kill metric

        if potential == -1:  # check if this pawn has already reached home
            continue

        if potential > maxPotential:  # metric > prev Metrics?
            maxPotential = potential

        playablePawns[potential].append(pawn.pawnId)  # store the pawn id according to its potential


    # NOTE the dict would never be empty when home stretch and six reqd is false
    if maxPotential == -1:  # handles cases when either six is reqd or home stretch is enabled

        pawnToMove = fastAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)

    elif maxPotential == 0:  # if no instant kills available, find chase

        newPawns = []
        for pawnId in playablePawns[maxPotential]:  # auto removes any pawns who might have completed the journey of life
            newPawns.append(pawns[pawnId])


        # Find Pawns valid for Chasing
        possibleChasers = []
        for pawn in newPawns:
            canChase = calcChaseMetric(pawn)  # chase metric returns the distance

            if canChase == -1:  # check if pawn doesn't chases
                continue

            possibleChasers.append(pawn.pawnId)  # store the pawn id according to its potential
            print()

        if possibleChasers == []:
            pawnToMove = fastAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)

        else:
            newPawns = []
            for pawnId in possibleChasers:  # cutshort the pawns array to only store pawns with the max potential
                newPawns.append(pawns[pawnId])

            myNewPlayer = (player, newPawns)
            pawnToMove = fastAlgo(game, myNewPlayer, boardDict, safeSpots, referenceDiff, diceNo)

    else:  # if kill available
        if len(playablePawns[maxPotential]) == 1:  # check if no clashes on max potential pawn
            pawnToMove = playablePawns[maxPotential][0]
        else:  # if clash while killing
            newPawns = []
            for pawnId in playablePawns[maxPotential]:  # cutshort the pawns array to only store pawns with the max potential
                newPawns.append(pawns[pawnId])

            myNewPlayer = (player, newPawns)
            pawnToMove = fastAlgo(game, myNewPlayer, boardDict, safeSpots, referenceDiff, diceNo)
            # use the fast algo to decide which pawn to move when both have positive and equal potential to kill

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

        # game.printState(myPlayer, boardDict, safeSpots, referenceDiff, diceNo)

        # print("Dice roll:",diceNo)
        print(myPlayer[0].C)
        p = agressiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        # print("Turn over")
        done = game.movePawn(int(p), diceNo)
        if done > -1:
            print("Player", done, "Won")
            break
        # time.sleep(0.5)

