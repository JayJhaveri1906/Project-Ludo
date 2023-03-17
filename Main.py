from Algo_Fast import fastAlgo
from Algo_Agressive import agressiveAlgo
from Algo_Defensive import defensiveAlgo
from Algo_Random import randomAlgo
from Algo_Mix import mixAlgo
from Game import Board, humanAlgo

config = []
runCount = 10000
winners = []

## Config - [pawns per player, strategy1, strategy2, ...]


config = [4, defensiveAlgo, fastAlgo, fastAlgo, randomAlgo]


if __name__ == "__main__":
    strategies = [humanAlgo, randomAlgo, fastAlgo, agressiveAlgo, defensiveAlgo, mixAlgo]

    if(config == []):
        players = int(input("Enter Number of Players: "))
        pawns = int(input("Enter Number of Pawns per Player: "))
        playerStrategies = []
        for i in range(players):
            strategy = int(input("Enter strategy for player " + str(i) + ": 0 for human, 1 for random, 2 for fast, 3 for aggressive, 4 for defensive, 5 for mix"))
            if(strategy not in {0,1,2,3,4,5}):
                print("Not a valid option, defaulting to random")
                strategy = 1
            playerStrategies.append(strategies[strategy])
        print("Debug mode? Enter y for true")
        debug = input()
        if debug not in {"y", "Y"}:
            debug = False
        else:
            debug = True
    else:
        players = len(config) - 1
        pawns = config[0]
        playerStrategies = config[1:]
        debug = False

    if(not config):
        runCount = 1

    for run in range(runCount):

        game = Board(players, pawns)
        # game.getNewState()

        while True:
            if(debug):
                input()
            myPlayer, boardDict, safeSpots, referenceDiff, diceNo = game.getNewState()
            if(debug):
                game.printState(myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
            p = playerStrategies[myPlayer[0].C](game, myPlayer, boardDict, safeSpots, referenceDiff, diceNo)
            done = game.movePawn(int(p), diceNo)
            if done > -1:
                winners.append(done)
                # print("Player", done, "Won")
                break
    
    print("\n\nWINNERS:")
    print(winners)
    print("0:", winners.count(0))
    print("1:", winners.count(1))
    print("2:", winners.count(2))
    print("3:", winners.count(3))