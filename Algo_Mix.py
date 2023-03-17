from Game import Board
from Algo_Fast import fastAlgo
from collections import defaultdict

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

    player = myPlayer[0]  # Extracting player
    pawns = myPlayer[1]  # Extracting the pawns

    playablePawns = []
    for pawn in pawns:
        if pawn.pi > (game.boardSize - 2):
            continue
        playablePawns.append(pawn)


    moreAdvantageDict = defaultdict(list)
    maxAdv = float("-inf")
    for pawn in playablePawns:
        past_risk = risk_curr(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawn)
        future_risk = risk_next(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawn)
        past_reward = reward_curr(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawn)
        future_reward = reward_next(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawn)

        MoveAdvantage = (future_reward - future_risk) - (past_reward - past_risk)

        if MoveAdvantage > maxAdv:
            maxAdv = MoveAdvantage

        moreAdvantageDict[str(MoveAdvantage)].append(pawn.pawnId)

    if len(moreAdvantageDict[str(maxAdv)]) == 1:  # check if no clashes on max potential pawn
        pawnToMove = moreAdvantageDict[str(maxAdv)][0]
    else:  # if clash while killing
        newPawns = []
        for pawnId in moreAdvantageDict[str(maxAdv)]:  # cutshort the pawns array to only store pawns with the max potential
            newPawns.append(pawns[pawnId])

        myNewPlayer = (player, newPawns)
        pawnToMove = fastAlgo(game, myNewPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        # use the fast algo to decide which pawn to move when both have positive and equal potential to kill

    return pawnToMove



def risk_curr(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawnP):
    pos = pawnP.pi
    if (pos > (game.boardSize - 2)):
        return 0
    p_alive = 1 
    for i in range(1,7):
        if boardDict[pos + i] != set():
            for elem in boardDict[pos + i]:
                if elem!= (pawnP.playerId, pawnP.pawnId):
                    p_alive *= (1-kill_board[str(i)])

    p_dying = 1 - p_alive
    risk = (pos in safeSpots)*pos*p_dying
    return risk


def risk_next(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawnP):
    pos = pawnP.pi + diceNo
    if (pos > (game.boardSize - 2)):
        return 0
    p_alive = 1 
    for i in range(1,7):
        if boardDict[pos + i] != set():
            for elem in boardDict[pos + i]:
                if elem!= (pawnP.playerId, pawnP.pawnId):
                    p_alive *= (1-kill_board[str(i)])

    p_dying = 1 - p_alive
    risk = (pos in safeSpots)*pos*p_dying
    return risk + diceNo

def reward_curr(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawnP):
    # Initialize an empty list to store the rewards for each pawn
    pos = pawnP.pi 
    reward = 0
    for i in range(1, 7):
        if boardDict[pos + i] != set():
            for elem in boardDict[pos + i]:
                if elem!= (pawnP.playerId, pawnP.pawnId):
                    player_of_pawn = game.players[elem[0]][1]
                    reward += kill_board[str(i)] * player_of_pawn[elem[1]].pi
    return reward


# takes dice roll + 3.5 * instantkill (bool) + sum starting from 0
def reward_next(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawnP):
    pos = pawnP.pi + diceNo

    if pos > game.boardSize - 2:
        return diceNo

    reward = 0
    for i in range(0, 7):
        if boardDict[pos + i] != set():
            for elem in boardDict[pos + i]:
                if elem!= (pawnP.playerId, pawnP.pawnId):
                    if i == 0:
                        reward += 3.5
                    else:
                        player_of_pawn = game.players[elem[0]][1]
                        reward += kill_board[str(i)] * player_of_pawn[elem[1]].pi
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

        # game.printState(myPlayer, boardDict, safeSpots, referenceDiff, diceNo)

        p = mixAlgo(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        done = game.movePawn(int(p), diceNo)
        if done > -1:
            print("Player", done, "Won")
            break