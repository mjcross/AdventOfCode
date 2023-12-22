from utils.grid import Grid, gridFromstream
from enum import Enum

class Heading(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)


def beam(x, y, heading, grid, tiles, pathN, pathE, pathS, pathW):
    count = 0
    try:
        while True:
            c = grid[x, y]

            if tiles[x, y] == ' ':
                count += 1
                tiles[x, y] = '#'

            if heading is Heading.N:
                if (x, y) in pathN:
                    return count    # loop detected
                else:
                    pathN.append((x, y))

                if c == '\\':
                    heading = Heading.W
                elif c == '/':
                    heading = Heading.E
                elif c == '-':
                    count += beam(x+1, y, Heading.E, grid, tiles, pathN, pathE, pathS, pathW)
                    count += beam(x-1, y, Heading.W, grid, tiles, pathN, pathE, pathS, pathW)
                    return count

            elif heading is Heading.E:
                if (x, y) in pathE:
                    return count    # loop detected
                else:
                    pathE.append((x, y))

                if c == '\\':
                    heading = Heading.S
                elif c == '/':
                    heading = Heading.N
                elif c == '|':
                    count += beam(x, y+1, Heading.N, grid, tiles, pathN, pathE, pathS, pathW)
                    count += beam(x, y-1, Heading.S, grid, tiles, pathN, pathE, pathS, pathW)
                    return count
                
            elif heading is Heading.S:
                if (x, y) in pathS:
                    return count    # loop detected
                else:
                    pathS.append((x, y))

                if c == '\\':
                    heading = Heading.E
                elif c == '/':
                    heading = Heading.W
                elif c == '-':
                    count += beam(x+1, y, Heading.E, grid, tiles, pathN, pathE, pathS, pathW)
                    count += beam(x-1, y, Heading.W, grid, tiles, pathN, pathE, pathS, pathW)
                    return count
                
            elif heading is Heading.W:
                if (x, y) in pathW:
                    return count    # loop detected
                else:
                    pathW.append((x, y))

                if c == '\\':
                    heading = Heading.N
                elif c == '/':
                    heading = Heading.S
                elif c == '|':
                    count += beam(x, y+1, Heading.N, grid, tiles, pathN, pathE, pathS, pathW)
                    count += beam(x, y-1, Heading.S, grid, tiles, pathN, pathE, pathS, pathW)
                    return count

            dx, dy = heading.value
            x += dx
            y += dy

            #print(f"({x}, {y}): {heading.name}: '{c}'")
            #print(tiles)

    except IndexError:
        pass

    return count


def part1(stream):
    grid = gridFromstream(stream)
    tiles = Grid(width=grid.width, height=grid.height)
    return beam(0, grid.height - 1, Heading.E, grid, tiles, [], [], [], [])


def part2(stream):
    grid = gridFromstream(stream)
    maxTiles = 0

    # southern edge
    for x in range(grid.width):
        tiles = Grid(width=grid.width, height=grid.height)
        maxTiles = max(maxTiles, beam(x, 0, Heading.N, grid, tiles, [], [], [], []))

    # western edge
    for y in range(grid.height):
        tiles = Grid(width=grid.width, height=grid.height)
        maxTiles = max(maxTiles, beam(0, y, Heading.E, grid, tiles, [], [], [], []))

    # northern edge
    for x in range(grid.width):
        tiles = Grid(width=grid.width, height=grid.height)
        maxTiles = max(maxTiles, beam(x, grid.height - 1, Heading.S, grid, tiles, [], [], [], []))

    # eastern edge
    for y in range(grid.height):
        tiles = Grid(width=grid.width, height=grid.height)
        maxTiles = max(maxTiles, beam(grid.width - 1, y, Heading.W, grid, tiles, [], [], [], []))    

    return maxTiles

def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 46, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 51, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()