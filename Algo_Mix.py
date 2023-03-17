from Game import Board

kill_board = {
    "0" : 1,
    "1" : 0.5,
    "2" : 5/12,
    "3" : 4/12,
    "4" : 3/12,
    "5" : 2/12,
    "6" : 1/12
 }

def mixAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo):
    # TODO: algorithm
    # TODO: you may use the game.get_reward and game.get_risk functions


    pawnToMove = -1
    return pawnToMove

def risk_curr(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, kill_board, pawnP):
    pos = pawnP.pi
    if (pos > (game.boardSize - 2)):
        return 0
    p_alive = 1 
    for i in range(1,7):
        if boardDict[pos + i] != set():
            for elem in boardDict[pos + i]:
                if elem[0]!= pawnP.playerId:
                    p_alive *= (1-kill_board[i])

    p_dying = 1 - p_alive
    risk = (pos in safeSpots)*pos*p_dying
    return risk


def risk_next(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, kill_board, pawnP):
    pos = pawnP.pi + diceNo
    if (pos > (game.boardSize - 2)):
        return diceNo
    p_alive = 1 
    for i in range(1,7):
        if boardDict[pos + i] != set():
            for elem in boardDict[pos + i]:
                if elem[0]!= pawnP.playerId:
                    p_alive *= (1-kill_board[i])

    p_dying = 1 - p_alive
    risk = (pos in safeSpots)*pos*p_dying
    return risk + diceNo

def reward_curr(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, kill_board, pawnP):
    # Initialize an empty list to store the rewards for each pawn
    pos = pawnP.pi 
    reward = 0
    for i in range(1, 7):
        if boardDict[pos + i] != set():
            for elem in boardDict[pos + i]:
                if elem[0] != pawnP.playerId:
                    reward += kill_board[str(i)] * elem.pi
    return reward


# takes dice roll + 3.5 * instantkill (bool) + sum starting from 0
def reward_next(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, kill_board, pawnP):
    pos = pawnP.pi + diceNo

    if pos > game.BoardSize - 2:
        return diceNo

    reward = 0
    for i in range(0, 7):
        if boardDict[pos + i] != set():
            for elem in boardDict[pos + i]:
                if elem[0] != pawnP.playerId:
                    if i == 0:
                        reward += 3.5
                    else:
                        reward += kill_board[str(i)] * elem.pi
    return reward + diceNo



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