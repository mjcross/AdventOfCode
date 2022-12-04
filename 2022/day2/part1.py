from enum import Enum

class Symbol(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

symbolScore = {
    Symbol.ROCK: 1,
    Symbol.PAPER: 2,
    Symbol.SCISSORS: 3
}

class Result(Enum):
    WIN = 0
    DRAW = 1
    LOSE = 2

resultScore = {
    Result.WIN: 6,
    Result.DRAW: 3,
    Result.LOSE: 0
}

beats = {
    Symbol.ROCK: Symbol.SCISSORS,
    Symbol.PAPER: Symbol.ROCK,
    Symbol.SCISSORS: Symbol.PAPER
}

letter = {
    'A': Symbol.ROCK, 
    'B': Symbol.PAPER, 
    'C': Symbol.SCISSORS, 
    'X': Symbol.ROCK, 
    'Y': Symbol.PAPER, 
    'Z': Symbol.SCISSORS
}

def main():
    myScore = 0
    with open('input.txt') as input:
        for line in input:
            theirGo = letter[line[0]]
            myGo = letter[line[2]]

            if myGo == theirGo:
                result = Result.DRAW
            elif theirGo == beats[myGo]:
                result = Result.WIN
            else:
                result = Result.LOSE
            
            myScore += symbolScore[myGo] + resultScore[result]

            print(f'they play {theirGo.name} I play {myGo.name}, I {result.name} scoring {symbolScore[myGo]} + {resultScore[result]} total {myScore}')

if __name__ == '__main__':
    main()