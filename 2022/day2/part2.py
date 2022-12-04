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

toLoseTo = {
    Symbol.ROCK: Symbol.SCISSORS,
    Symbol.PAPER: Symbol.ROCK,
    Symbol.SCISSORS: Symbol.PAPER
}

toBeat = {
    Symbol.SCISSORS: Symbol.ROCK,
    Symbol.PAPER: Symbol.SCISSORS,
    Symbol.ROCK: Symbol.PAPER
}

symbolForLetter = {
    'A': Symbol.ROCK, 
    'B': Symbol.PAPER, 
    'C': Symbol.SCISSORS, 
}

resultForLetter = {
    'X': Result.LOSE,
    'Y': Result.DRAW,
    'Z': Result.WIN
}

def main():
    myScore = 0
    with open('input.txt') as input:
        for line in input:
            theirGo = symbolForLetter[line[0]]
            result = resultForLetter[line[2]]

            myGo = theirGo
            if result == Result.WIN:
                myGo = toBeat[theirGo]
            elif result == Result.LOSE:
                myGo = toLoseTo[theirGo]
            
            myScore += symbolScore[myGo] + resultScore[result]

            print(f'they play {theirGo.name} I play {myGo.name}, I {result.name} scoring {symbolScore[myGo]} + {resultScore[result]} total {myScore}')

if __name__ == '__main__':
    main()