from parse import parse
from pipe import Pipe, pipes, Dir
from listgrid import ListGrid

def part1(stream):
    txtgrid = parse(stream)
    x, y = txtgrid.find('S')

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
    

def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 8, result

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    print(f'example2: {result}')
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    #with open('input.txt') as stream:
    #    result = part2(stream)
    #    print(f'part2 {result}')


if __name__ == '__main__':
    main()