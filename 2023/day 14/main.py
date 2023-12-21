from utils.grid import Grid, gridFromstream

def northLoad(grid):
    """
    Calculate the load on the Northern support beam
    without making any changes to the grid.
    """
    load = 0
    for x in range(grid.width):
        top = grid.height   # maximum row a rock can slide up to
        for y in reversed(range(grid.height)):
            c = grid[x, y]
            if c == 'O':
                load += top # add load due to where this rock can slide to
                top -= 1    # next rock can slide up to this one
            elif c == '#':
                top = y     # next rock can only slide up to here
    return load

def load(grid):
    load = 0
    for x in range(grid.width):
        for y in range(grid.height):
            if grid[x, y] == 'O':
                load += y + 1
    return load

def part1(stream):
    grid: Grid = gridFromstream(stream)
    return northLoad(grid)

def north(grid: Grid):
    for x in range(grid.width):
        top = grid.height - 1
        for y in reversed(range(grid.height)):
            c = grid[x, y]
            if c == 'O':
                grid[x, y] = '.'
                grid[x, top] = 'O'
                top -= 1
            elif c == '#':
                top = y - 1
    return grid

def east(grid: Grid):
    for y in range(grid.height):
        top = grid.width - 1
        for x in reversed(range(grid.width)):
            c = grid[x, y]
            if c == 'O':
                grid[x, y] = '.'
                grid[top, y] = 'O'
                top -= 1
            elif c == '#':
                top = x - 1
    return grid

def south(grid: Grid):
    for x in range(grid.width):
        top = 0
        for y in range(grid.height):
            c = grid[x, y]
            if c == 'O':
                grid[x, y] = '.'
                grid[x, top] = 'O'
                top += 1
            elif c == '#':
                top = y + 1
    return grid

def west(grid: Grid):
    for y in range(grid.height):
        top = 0
        for x in range(grid.width):
            c = grid[x, y]
            if c == 'O':
                grid[x, y] = '.'
                grid[top, y] = 'O'
                top += 1
            elif c == '#':
                top = x + 1
    return grid

def spin(grid: Grid):
    north(grid)
    west(grid)
    south(grid)
    east(grid)
    return grid

def part2(stream):
    grid: Grid = gridFromstream(stream)

    # allow a sequence to develop
    warmup = 1000
    for _ in range(warmup):
        spin(grid)
    
    # see how long it takes to get back to the same state
    maxPeriod = 100
    a = tuple(grid._array)
    for nSpins in range(maxPeriod):
        spin(grid)
        if tuple(grid._array) == a:
            break
    else:
        raise ValueError('no repeats found in ', maxPeriod)
    period = nSpins
    print('period', nSpins)

    target = 1000000000
    target -= warmup

    for nSpins in range(target % (period + 1)):
        print(nSpins, load(grid))
        spin(grid)
    
    return load(grid)


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 136, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
    #    assert result == 'xxxxx', result


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