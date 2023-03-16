from Game import Board
from Algo_Fast import fastAlgo
from collections import defaultdict
import time


def agressiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
    # TODO: algorithm
    # TODO: you may use the game.get_reward and game.get_risk functions
    # My Priority in Agressiveness
    ##  1) If instant kill, then kill
    ##      a) Have weighted kills (smart aggressive) cancel here
    ##  2) else: move the one that is closest to enemey
    ##      a) Here to it should be weighted as in I should prioritze the enemey which is closer to its home

    # NOTE: Only looking one step into the future currently
    pawnToMove = -1  # Final pawn to move
    usedFastAsDefault = False  # did you used fast algo as a default

    # Calculates kill potential
    def calcKillMetric(pawn):
        if pawn.pi == -1:
            return -1
        gpos = game.getGlobalPos(pawn.playerId, pawn.pi)  # get gPos
        gpos += diceNo  # new pos

        enemy_count = 0
        if gpos not in safeSpots and gpos not in referenceDiff:  # Check if not on safe spot
            for pawns in boardDict[gpos]:
                if pawns.playerId != pawn.playerId:
                    enemy_count += 1  # count how many enemey players you can kill

        return enemy_count

    # Calculates chase potential
    def calcChaseMetric(pawn):
        gpos = game.getGlobalPos(pawn.playerId, pawn.pi)  # get gPos
        gpos += diceNo  # new pos
        start_pos_of_pawn = referenceDiff[pawn.playerId]
        end_pos_of_pawn = start_pos_of_pawn + game.boardSize

        dist_between = -1
        cnt = gpos+1
        while cnt != end_pos_of_pawn:
            for pawns in boardDict[gpos]:
                if pawns.playerId != pawn.playerId:
                    break
        # TODO: handle the condition ki basically impleent difference in distance before and after... if decreasing distance then potential is the dist.... basically....



        return enemy_count

    player = myPlayer[0]  # Extracting player
    pawns = myPlayer[1]  # Extracting the pawns

    dict = defaultdict(list)  # dictionary to store pawn id wrt their potentials
    maxPotential = -1  # max potential to have O(1) access to the max potential pawn

    for pawn in pawns:
        potential = calcKillMetric(pawn)  # kill metric

        if potential == -1:  # check if this pawn has already reached home
            continue

        if potential > maxPotential:  # metric > prev Metrics?
            maxPotential = potential

        dict[potential].append(pawn.pawnId)  # store the pawn id according to its potential

    # NOTE the dict would never be empty when home stretch and six reqd is false
    if maxPotential == -1:  # handles cases when either six is reqd or home stretch is enabled
        usedFastAsDefault = True
        pawnToMove = fastAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)

    elif maxPotential == 0:  # if no kills available, find chase

        newPawns = []
        for pawnId in dict[maxPotential]:  # auto removes any pawns who might have completed the journey of life
            newPawns.append(pawns[pawnId])



        for pawn in newPawns:
            potential = calcKillMetric(pawn)  # kill metric

            if potential == -1:  # check if this pawn has already reached home
                continue

            if potential > maxPotential:  # metric > prev Metrics?
                maxPotential = potential

            dict[potential].append(pawn.pawnId)  # store the pawn id according to its potential


        usedFastAsDefault = True
        pawnToMove = fastAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
    else:
        if len(dict[maxPotential]) == 1:  # check if no clashes on max potential pawn
            pawnToMove = dict[maxPotential][0]
        else:  # if clash while killing
            newPawns = []
            for pawnId in dict[maxPotential]:  # cutshort the pawns array to only store pawns with the max potential
                newPawns.append(pawns[pawnId])

            myNewPlayer = (player, newPawns)
            pawnToMove = fastAlgo(game, myNewPlayer, boardDict, safeSpots, referenceDiff, diceNo)
            # use the fast algo to decide which pawn to move when both have positive and equal potential to kill

    return pawnToMove, usedFastAsDefault


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

        # print("Dice roll:",diceNo)
        p, _ = agressiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        done = game.movePawn(int(p), diceNo)
        if done > -1:
            print("Player", done, "Won")
            break
        # time.sleep(0.5)

