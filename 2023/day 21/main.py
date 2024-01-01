from parse import parse
from enum import Enum
from grid import Grid

class Move(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)


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

        # print(grid)
        plots = nextPlots
        nNewPlots.append(len(nextPlots))

    return calcN(nSteps, nNewPlots)


def calcN(nSteps, nNew):
    return sum(nNew[nSteps % 2: nSteps + 1: 2])


def part2(stream, nSteps):
    baseGrid, baseStart = parse(stream)
    assert baseGrid.width == baseGrid.height    # the map must tessalate
    baseWidth = baseGrid.width

    # add three copies of the map in each direction
    grid = Grid(7 * baseWidth, 7 * baseWidth)
    for y in range(grid.height):
        for x in range(grid.width):
            grid[x, y] = baseGrid[x % baseWidth, y % baseWidth]
    start = (baseStart[0] + baseGrid.width * 3, baseStart[1] + baseGrid.height * 3)

    # calculate the number of plots that can be reached in 'n' steps, up to the edge of the 3-copy map
    plots = [start]
    nNewPlots = [0]
    N = [0]
    sumEven = 0
    sumOdd = 0
    # breadth-first search
    for stepCounter in range(1, 65 + (3 * baseWidth) + 1):
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
        nNewPlots.append(len(nextPlots))

        # for an even numbers of steps the number of plots visitable 
        # is the sum of the new places reachable with even numbers of steps
        if stepCounter % 2 == 0:
            sumEven += len(nextPlots)
            N.append(sumEven)
        else:
            # for an odd number of steps, it's the sum of the places reachable 
            # with odd numbers of steps
            sumOdd += len(nextPlots)
            N.append(sumOdd)

    assert N[64] == part1(stream, 64), 'match part1 result'

    # Because the map is tessalated we should have some basic symmetries for each 'ring' of map copies.
    # We have generated the data for three such rings.
            
    # work out how the number of plots increases across a while ring
    # - it should increase linearly
    ringDiffs = []
    for ringIndex in range(3):
        ringStart = 65 + ringIndex * baseWidth
        ringEnd = ringStart + baseWidth - 1
        ringDiffs.append(N[ringEnd] - N[ringStart])
    ringDiff = ringDiffs[0]
    assert ringDiffs[1] == 2 * ringDiff, 'linear increase per ring'
    assert ringDiffs[2] == 3 * ringDiff, 'linear increase per ring'
    print('\tringDiff:', ringDiff)

    # we can do a fracional final ring but it's not required for the puzzle
    assert (nSteps - 65) % baseWidth == 0, 'whole number of rings'
    nRings = (nSteps - 65) // baseWidth
    print('\tnRings:', nRings)

    # work out how the gap between the start of one ring and the next changes 
    # - it should be a linear increase plus an offset
    ringGaps = []
    for ringIndex in range(3):
        ringStart = 65 + (ringIndex * baseWidth)
        ringGaps.append(N[ringStart] - N[ringStart - 1])
    ringGapOffset = ringGaps[0]
    ringGapDiff = ringGaps[1] - ringGaps[0]
    assert ringGaps[2] == ringGapOffset + 2 * ringGapDiff
    print(f'\tringGap: {ringGapOffset} + {ringGapDiff}')

    # there will be a way to do this algebraically, but...
    nPlots = N[65]
    for ringIndex in range(nRings):
        # cross the ring
        nPlots += ringDiff * (ringIndex + 1)

        # cross the gap to the next ring
        nPlots += ringGapOffset + ringGapDiff * (ringIndex + 1)

    return nPlots


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream, 6)
        print(f'example1: {result}')
    #    assert result == 'xxxxx', result

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    print(f'example2: {result}')
    #    assert result == 'xxxxx', result


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