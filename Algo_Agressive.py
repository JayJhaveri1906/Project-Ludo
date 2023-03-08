from Game import Board
from Algo_Fast import fastAlgo


def agressiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
    # TODO: algorithm
    # TODO: you may use the game.get_reward and game.get_risk functions

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

    player = myPlayer[0]  # Extracting player
    pawns = myPlayer[1]  # Extracting the pawns

    dict = {}  # dictionary to store pawn id wrt their potentials
    maxPotential = float("-inf")  # max potential to have O(1) access to the max potential pawn

    for pawn in pawns:
        potential = calcKillMetric(pawn)  # kill metric
        if potential > maxPotential:  # metric > prev Metrics?
            maxPotential = potential

        dict[potential] = pawn.pawnId  # store the pawn id according to its potential

    if len(dict[maxPotential]) == 1:  # check if no clashes on max potential pawn
        pawnToMove = dict[maxPotential]
    else:  # if clash
        if maxPotential == 0 or maxPotential == -1:  # if clash when kill potential is 0, or all pawns are in home (hence -1) use the fast algo
            usedFastAsDefault = True
            pawnToMove = fastAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        else:  # if clash when killing potential > 0
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

        p, _ = agressiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        game.movePawn(int(p), diceNo)
