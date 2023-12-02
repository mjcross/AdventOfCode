from parse import parse
from game import Turn

def part1(stream, maxCounts):
    """Returns the sum of the IDs of games possible with maxCounts cubes."""
    games = parse(stream)
    idSum = 0
    for game in games:
        try:
            for turn in game.turns:
                if turn > maxCounts:
                    # this turn was not possible => then game was not possible
                    raise ValueError
            # all turns were possible => the game was possible
            idSum += game.id
        except ValueError:
            # this game was not possible
            continue

    return idSum


def part2(stream):
    """Returns the sum of the products of the minimum numbers of cubes for each game."""
    games = parse(stream)
    powerSum = 0
    for game in games:
        maxCounts = Turn()
        for turn in game.turns:
            maxCounts.red = max(turn.red, maxCounts.red)
            maxCounts.green = max(turn.green, maxCounts.green)
            maxCounts.blue = max(turn.blue, maxCounts.blue)
        power = maxCounts.red * maxCounts.green * maxCounts.blue
        powerSum += power
    return powerSum


def checkexamples(part1Counts):
    with open('example.txt') as stream:
        result = part1(stream, part1Counts)
        print(f'example1: {result}')
        assert result == 8, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 2286, result


def main():
    part1Counts = Turn(red=12, green=13, blue=14)
    checkexamples(part1Counts)

    with open('input.txt') as stream:
        result = part1(stream, part1Counts)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()