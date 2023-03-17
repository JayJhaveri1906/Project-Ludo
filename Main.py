from Algo_Fast import fastAlgo
from Algo_Agressive import agressiveAlgo
from Algo_Defensive import defensiveAlgo
from Algo_Random import randomAlgo
from Algo_Mix import mixAlgo
from Game import Board, humanAlgo

if __name__ == "__main__":
    strategies = [humanAlgo, randomAlgo, fastAlgo, agressiveAlgo, defensiveAlgo, mixAlgo]
    players = int(input("Enter Number of Players: "))
    pawns = int(input("Enter Number of Pawns per Player: "))
    playerStrategies = []
    for i in range(players):
        strategy = int(input("Enter strategy for player " + str(i) + ": 0 for human, 1 for random, 2 for fast, 3 for aggressive, 4 for defensive, 5 for mix"))
        if(strategy not in {0,1,2,3,4,5}):
            print("Not a valid option, defaulting to random")
            strategy = 1
        playerStrategies.append(strategies[strategy])

    game = Board(players, pawns)
    # game.getNewState()

    print("Debug mode? Enter y for true")
    debug = input()
    if debug not in {"y", "Y"}:
        debug = False
    else:
        debug = True

    while True:
        if(debug):
            input()
        myPlayer, boardDict, safeSpots, referenceDiff, diceNo = game.getNewState()
        game.printState(myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        p = playerStrategies[myPlayer[0].C](game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
        print("Moving ", p)
        done = game.movePawn(int(p), diceNo)
        if done > -1:
            print("Player", done, "Won")
            break
