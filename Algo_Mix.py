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
        # print(pawn, past_risk, future_risk, past_reward, future_reward)

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
        if boardDict[(pos - i)%52] != set():                     ## BUG? - Checking behind in global pos without %52?
            for elem in boardDict[(pos - i)%52]:
                if elem[0] == pawnP.playerId:
                    continue
                if elem!= (pawnP.playerId, pawnP.pawnId):   ## BUG? - Checking if elem is not pawn itself? Why? Check if not other pawn of same player. Also, check if that pawn is going to go into its own home before striking. In that case also ignore
                    p_alive *= (1-kill_board[str(i)])

    p_dying = 1 - p_alive
    risk = (pos not in safeSpots)*pos*p_dying
    ## SUGGEST risk = (pos not in safeSpots)*pos*p_dying*0.5 + 1*(pos not in safeSpots)
    return risk


def risk_next(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawnP):
    pos = pawnP.pi + diceNo
    if (pos > (game.boardSize - 2)):
        return 0
    p_alive = 1 
    for i in range(1,7):
        if boardDict[(pos - i)%52] != set():
            for elem in boardDict[(pos - i)%52]:
                if elem[0] == pawnP.playerId:
                    continue
                if elem!= (pawnP.playerId, pawnP.pawnId):      ## BUG? - Same as in risk_curr function
                    p_alive *= (1-kill_board[str(i)])

    p_dying = 1 - p_alive
    risk = (pos not in safeSpots)*pos*p_dying
    ## SUGGEST risk = (pos not in safeSpots)*pos*p_dying*0.5 + 1*(pos not in safeSpots)
    return risk                ## BUG? - Why diceNo?

def reward_curr(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawnP):
    # Initialize an empty list to store the rewards for each pawn
    pos = pawnP.pi 
    reward = 0
    for i in range(1, 7):
        if boardDict[(pos + i)%52] != set():                    ## BUG? If position is a safe spot, no kills possible
            if((pos + i)%52 in safeSpots):
                continue
            for elem in boardDict[(pos + i)%52]:
                if elem[0] == pawnP.playerId:
                    continue
                if elem!= (pawnP.playerId, pawnP.pawnId):       ## BUG? Just what is this check? Refer BUG? in risk_curr function
                    player_of_pawn = game.players[elem[0]][1]
                    reward += kill_board[str(i)] * player_of_pawn[elem[1]].pi
    return reward
## SUGGEST return reward*4


# takes dice roll + 3.5 * instantkill (bool) + sum starting from 0
def reward_next(game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo, pawnP):
    pos = pawnP.pi + diceNo

    if pos > game.boardSize - 2:
        return diceNo

    reward = 0
    for i in range(0, 7):
        if boardDict[(pos + i)%52] != set():                    ## BUG? If position is a safe spot, no kills possible
            if((pos + i)%52 in safeSpots):
                continue
            for elem in boardDict[(pos + i)%52]:
                if elem[0] == pawnP.playerId:
                    continue
                if elem!= (pawnP.playerId, pawnP.pawnId):   ## BUG? - Again, same thing. Refer risk_curr BUG?
                    if i == 0:
                        reward += 3.5                       ## BUG? - In case of strike, reward includes value of pawn struck, like below. Add the struck pawn's pi. This is choosing not to strike.
                    # else:
                    player_of_pawn = game.players[elem[0]][1]
                    reward += kill_board[str(i)] * player_of_pawn[elem[1]].pi
    return reward
## SUGGEST return reward*4 + diceNo

## BUG buggish - reduce risk perception, increase efforts for chase and fast. Also make a slight incentive for actual safespot in risk even without any chasers.

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