from parse import parse, parse2
from itertools import combinations


def part1(stream):
    grid = parse(stream)
    galaxies = grid.findAll('#')
    sum = 0
    for g1, g2 in combinations(galaxies, 2):
        # their distance is equivalent to the taxicab distance
        sum += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    return sum


def part2(stream, expansion):
    grid, xLookup, yLookup = parse2(stream, expansion)
    # map galaxy coords to expanded frame
    galaxies = [(xLookup[x], yLookup[y]) for x, y in grid.findAll('#')]
    # now its the same as part(i)
    sum = 0
    for g1, g2 in combinations(galaxies, 2):
        # their distance is equivalent to the taxicab distance
        sum += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    return sum


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 374, result

    with open('example.txt') as stream:
        result = part2(stream, 10)
        print(f'example2a: {result}')
        assert result == 1030, result

        result = part2(stream, 100)
        print(f'example2b: {result}')
        assert result == 8410, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream, 1_000_000)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()