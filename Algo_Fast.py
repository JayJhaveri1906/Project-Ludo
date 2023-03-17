from Game import Board


def fastAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
    # TODO: algorithm
    # TODO: you may use the game.get_reward and game.get_risk functions
    localpawns = []
    if (not localpawns):
        for pawn in myPlayer[1]:
            if (pawn.pi > (game.boardSize - 2)):
                continue
            localpawns.append(pawn)

    if (not localpawns):
        return -1

    max_pawn = localpawns[0]
    for pawn in localpawns:
        if (pawn.pi > max_pawn.pi):
            max_pawn = pawn

    return max_pawn.pawnId


if __name__ == "__main__":
    players = int(input("Enter Number of Players: "))
    pawns = int(input("Enter Number of Pawns per Player: "))

    game = Board(players, pawns)

    while True:
        input()
        myPlayer, boardDict, safeSpots, referenceDiff, diceNo = game.getNewState()
        """ myPlayer: array of tuple of (playerObject, pawnsObjectArray)
        boardDict: mapping of each global position to a (playerNo, pawnNo) if on it
        safeSpots: set of safe Spots Global positions
        referenceDiff: list of spawn positions which are aso safe Spots
        diceNo: the dice number that came """

        game.printState(myPlayer, boardDict, safeSpots, referenceDiff, diceNo)

        p = fastAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        done = game.movePawn(int(p), diceNo)
        if done > -1:
            print("Player", done, "Won")
            break
