from Game import Board

def defensiveAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
    # TODO: algorithm
    # TODO: you may use the game.get_reward and game.get_risk functions


    pawnToMove = -1
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

        p = someAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        game.movePawn(int(p), diceNo)