from parse import parse
from pipe import Pipe, pipes, Dir
from listgrid import ListGrid

def part1(stream):
    txtgrid = parse(stream)
    x, y = txtgrid.find('S')

    # build grid of pipes from text grid
    grid = ListGrid(txtgrid.width, txtgrid.height, [pipes[chr(c)] for c in txtgrid._array])
    
    # find first step
    for dir in Dir:
        dx, dy = dir.dxdy
        if grid[x+dx, y+dy].isAccessibleHeading(dir):
            break
    else:
        raise ValueError('Cant find first step')

    # take first step
    x, y = x + dx, y + dy
    stepCount = 1

    # follow the pipe
    while grid[x, y].symbol != 'S':
        dir = grid[x, y].nextDir(dir)
        dx, dy = dir.dxdy
        x, y = x + dx, y + dy
        stepCount += 1
        assert grid[x, y].isAccessibleHeading(dir)

    # the furthest point is halfway around
    return stepCount // 2


def declutter(txtgrid):
    # build grid of pipes from text grid 
    grid = ListGrid(txtgrid.width, txtgrid.height, [pipes[chr(c)] for c in txtgrid._array])

    # find start point and direction
    x, y = txtgrid.find('S')
    for dir in Dir:
        dx, dy = dir.dxdy
        if grid[x+dx, y+dy].isAccessibleHeading(dir):
            startDir = dir
            break
    else:
        raise ValueError('Cant find first step')

    # clear text grid
    txtgrid._array = [ord('.')] * txtgrid.width * txtgrid.height

    # follow the pipe and draw it on the text grid
    x, y = x + dx, y + dy
    stepCount = 1
    pipe = grid[x, y]
    txtgrid[x, y] = pipe.symbol   # mark pipe on text grid
    while grid[x, y].symbol != 'S':
        dir = pipe.nextDir(dir)
        dx, dy = dir.dxdy
        x, y = x + dx, y + dy
        stepCount += 1
        pipe = grid[x, y]
        txtgrid[x, y] = pipe.symbol   # mark pipe on text grid
        assert pipe.isAccessibleHeading(dir)

    # replace start symbol with correct pipe
    for pipe in pipes.values():
        try:
            if pipe.nextDir(dir) is startDir:
                txtgrid[x, y] = pipe.symbol
                break
        except ValueError:
            pass

    return txtgrid


def part2(stream):
    grid = declutter(parse(stream))

    # count enclosed '.' tiles
    tileCount = 0
    for y in range(grid.height):
        isInside = False
        for x in range(grid.width):
            c = grid[x, y]
            if c in '|LJ':
                isInside = not isInside
            elif c == '.':
                if isInside:
                    tileCount += 1
                else:
                    grid[x, y] = ' '
    
    print(grid)
    return tileCount


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 8, result

    with open('example2.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 10, result


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