from enum import Enum
from dataclasses import dataclass
from utils.array2d import Array2D

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Item(Enum):
    LEFT = '<'
    RIGHT = '>'
    UP = '^'
    DOWN = 'v'
    SPACE = '.'
    WALL = '#'


class Move(Enum):
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    WAIT = Point(0, 0)

    def __repr__(self):
        return self.name


@dataclass(frozen=True)
class Blizzards:
    L: Array2D
    R: Array2D
    U: Array2D
    D: Array2D
    width: int
    height: int

    def __post_init__(self):
        # get around mutating a 'frozen' object (see https://stackoverflow.com/questions/53756788)
        object.__setattr__(self, 'start', Point(0, -1))
        object.__setattr__(self, 'end', Point(self.width - 1, self.height))

    def left(self, p, t):
        return self.L[(p.x + t) % self.width, p.y]

    def right(self, p, t):
        return self.R[(p.x - t) % self.width, p.y]

    def up(self, p, t):
        return self.U[p.x, (p.y + t) % self.height]

    def down(self, p, t):
        return self.D[p.x, (p.y - t) % self.height]

    def cell(self, p, t):
        if 0 <= p.x < self.width and 0 <= p.y < self.height:
            # blizzards at time t
            return self.left(p, t) or self.right(p, t) or self.up(p, t) or self.down(p, t)

        elif p == self.start or p == self.end:
            return 0

        else:
            # out of bounds
            return 2
            

def parse(stream):
    # blizzard coords at time zero
    left = []
    right = []
    up = []
    down = []
    for y, line in enumerate(stream, start=-1):
        for x, c in enumerate(line.rstrip(), start=-1):
            if c == Item.LEFT.value:
                left.append(Point(x, y))
            elif c == Item.RIGHT.value:
                right.append(Point(x, y))
            elif c == Item.UP.value:
                up.append(Point(x, y))
            elif c == Item.DOWN.value:
                down.append(Point(x, y))
    L = Array2D('B', 0, x-1, 0, y-1, 0)
    for p in left:
        L[p] = 1
    R = Array2D('B', 0, x-1, 0, y-1, 0)
    for p in right:
        R[p] = 1
    U = Array2D('B', 0, x-1, 0, y-1, 0)
    for p in up:
        U[p] = 1
    D = Array2D('B', 0, x-1, 0, y-1)
    for p in down:
        D[p] = 1
    return Blizzards(L=L, R=R, U=U, D=D, width=x, height=y)


def route(grid, start_pos, end_pos, start_time=0):
    t = start_time
    elves = {start_pos}   # NB: using set(grid.start) would unpack the tuple
    while end_pos not in elves:
        # print(f'Minute {t}: {len(elves)} elves')
        new_elves = set()
        for elf in elves:
            for move in Move:
                new_elf = elf + move.value
                if grid.cell(new_elf, t + 1) == 0:
                    new_elves.add(new_elf)
        elves = new_elves
        t += 1
    return t


def part1(stream):
    grid = parse(stream)
    return route(grid, grid.start, grid.end)


def part2(stream):
    grid = parse(stream)
    print('start -> end')
    t = route(grid, grid.start, grid.end, start_time=0)
    print(t)
    print('end -> start')
    t = route(grid, grid.end, grid.start, start_time=t)
    print(t)
    print('start -> end')
    t = route(grid, grid.start, grid.end, start_time=t)
    print(t)
    return t



def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 18, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 54, result


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