from array2d import Array2D
from iterate2d import iterate2d

AIR = ord('.')
ROCK = ord('#')
SAND = ord('o')
START = ord('+')


def showgrid(grid):
    for rowstart in range(0, len(grid._array), grid.width):
        print(''.join([chr(c) for c in grid._array[rowstart: rowstart + grid.width]]))


def parseminmax(stream):
    ymin = 0
    xmin = xmax = ymax = None
    for line in stream:
        pointlist = line.split(' -> ')
        for point in pointlist:
            x, y = map(int, point.split(','))
            if xmin is None or x < xmin:
                xmin = x
            if xmax is None or x > xmax:
                xmax = x
            if ymax is None or y > ymax:
                ymax = y
    return xmin, xmax, ymin, ymax


def parsegrid(stream, xmin, xmax, ymin, ymax):
    grid = Array2D('B', xmin, xmax, 0, ymax, AIR)

    pointlists = []
    for line in stream:
        pointlist = [map(int, point.split(',')) for point in line.split(' -> ')]
        pointlists.append(pointlist)

    for pointlist in pointlists:
        x1, y1 = pointlist.pop()
        while pointlist:
            x2, y2 = pointlist.pop()
            for x, y in iterate2d(x1, y1, x2, y2):
                grid[x, y] = ROCK
            x1, y1 = x2, y2
    
    return grid


def part1(stream, startx, starty):
    xmin, xmax, _, ymax = parseminmax(stream)
    stream.seek(0)
    grid = parsegrid(stream, xmin, xmax, starty, ymax)
    grid[startx, starty] = START

    sandcount = 0
    while True:
        x, y = startx, starty
        while True:
            try:
                if grid[x, y+1] == AIR:
                    y += 1
                elif grid[x-1, y+1] == AIR:
                    x -= 1
                    y += 1
                elif grid[x+1, y+1] == AIR:
                    x += 1
                    y += 1
                else:
                    grid[x, y] = SAND
                    break
            except IndexError:
                return sandcount
        sandcount += 1



def part2(stream, startx, starty):
    xmin, xmax, _, ymax = parseminmax(stream)
    stream.seek(0)
    ymax += 2
    grid = parsegrid(stream, startx - ymax, startx + ymax, starty, ymax)
    grid[startx, starty] = START
    for floorx in range(grid.xmin, 1 + grid.xmax):
        grid[floorx, ymax] = ROCK

    sandcount = 0
    while True:
        x, y = startx, starty
        while True:
            if grid[x, y+1] == AIR:
                y += 1
            elif grid[x-1, y+1] == AIR:
                x -= 1
                y += 1
            elif grid[x+1, y+1] == AIR:
                x += 1
                y += 1
            else:
                grid[x, y] = SAND
                if grid[startx, starty] == SAND:
                    sandcount += 1
                    showgrid(grid)
                    return sandcount
                break
        sandcount += 1
    


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream, 500, 0)
        assert example1 == 24, example1

    with open('example.txt') as stream:
        example2 = part2(stream, 500, 0)
        assert example2 == 93, example2


def main():
    checkexamples()

    with open('input.txt') as stream:
        print('part1', part1(stream, 500, 0))

    with open('input.txt') as stream:
        print('part2', part2(stream, 500, 0))


if __name__ == '__main__':
    main()