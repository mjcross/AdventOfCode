from parse import parse
from enum import Enum
from grid import Grid
from extrapolate import lagrangeInterpolate


class Move(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)


def calcN(nSteps, nNew):
    return sum(nNew[nSteps % 2: nSteps + 1: 2])


def part1(stream, nSteps):
    grid, start = parse(stream)
    
    plots = [start]
    nNewPlots = [0]
    for step in range(nSteps):

        nextPlots = []
        for plot in plots:
            x, y = plot
            for move in Move:
                dx, dy = move.value
                tryX = (x + dx) % grid.width
                tryY = (y + dy) % grid.height
                try:
                    if grid[tryX, tryY] == '.':
                        grid[tryX, tryY] = 'O'
                        nextPlots.append((tryX, tryY))
                except IndexError:
                    pass

        plots = nextPlots
        nNewPlots.append(len(nextPlots))

    return calcN(nSteps, nNewPlots)


def part2(stream, nSteps):
    baseGrid, baseStart = parse(stream)
    assert baseGrid.width == baseGrid.height    # the map must be square
    baseWidth = baseGrid.width

    # add two copies of the map in each direction
    grid = Grid(5 * baseWidth, 5 * baseWidth)
    for y in range(grid.height):
        for x in range(grid.width):
            grid[x, y] = baseGrid[x % baseWidth, y % baseWidth]
    start = (baseStart[0] + baseGrid.width * 2, baseStart[1] + baseGrid.height * 2)

    # calculate the number of plots that can be reached in 'n' steps, 
    # up to the edge of the extended map
    plots = [start]
    N = [0]
    sumEven = 0
    sumOdd = 0
    # breadth-first search
    for stepCounter in range(1, 65 + (2 * baseWidth) + 1):
        nextPlots = []
        for plot in plots:
            x, y = plot
            for move in Move:
                dx, dy = move.value
                tryX = x + dx
                tryY = y + dy
                try:
                    if grid[tryX, tryY] == '.':
                        grid[tryX, tryY] = 'O'
                        nextPlots.append((tryX, tryY))
                except IndexError:
                    pass

        plots = nextPlots

        if stepCounter % 2 == 0:
            # places reachable with an even number of steps
            sumEven += len(nextPlots)
            N.append(sumEven)
        else:
            # places reachable with an odd number of steps
            sumOdd += len(nextPlots)
            N.append(sumOdd)

    # interpolate based on the value at the edge of each 'ring'
    points = [(65 + n * baseWidth, N[65 + n * baseWidth]) for n in range(3)]
    return lagrangeInterpolate(points, 26_501_365)


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream, 6)
        print(f'example1: {result}')
        assert result == 16, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream, 64)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream, 26_501_365)
        print(f'part2 {result}')



if __name__ == '__main__':
    main()