from dataclasses import dataclass
from utils.array2d import Array2D
from copy import copy
from collections import namedtuple
from enum import Enum, IntEnum
from array import array
from itertools import cycle

class Item(IntEnum):
    SPACE = ord('.')
    ELF = ord('#')
    NONE = ord('-')

@dataclass(frozen=True)
class Neighbours:
    nw: int
    n:  int
    ne: int
    e:  int
    se: int
    s:  int
    sw: int
    w:  int

    def __iter__(self):
        return iter((self.nw, self.n, self.ne, self.e, self.se, self.s, self.sw, self.w))

    def can_move_n(self):
        return self.n != Item.ELF and self.ne != Item.ELF and self.nw != Item.ELF

    def can_move_s(self):
        return self.s != Item.ELF and self.se != Item.ELF and self.sw != Item.ELF

    def can_move_w(self):
        return self.w != Item.ELF and self.nw != Item.ELF and self.sw != Item.ELF

    def can_move_e(self):
        return self.e != Item.ELF and self.ne != Item.ELF and self.se != Item.ELF

    def count(self, item):
        count = 0
        for element in self:
            if element == item:
                count += 1
        return count



@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return(Point(self.x + other.x, self.y + other.y))

    def __iter__(self):
        return iter((self.x, self.y))


class Direction(Enum):
    NW = Point(-1, -1)
    N  = Point(0, -1)
    NE = Point(1, -1)
    E  = Point(1, 0)
    SE = Point(1, 1)
    S  = Point(0, 1)
    SW = Point(-1, 1)
    W  = Point(-1, 0)

    def __repr__(self):
        return self.name


@dataclass
class Elf:
    pos: Point


class Grid(Array2D):
    def __init__(self, typecode='i', xmin=0, xmax=0, ymin=0, ymax=0, initialvalue=0):
        super().__init__(typecode, xmin, xmax, ymin, ymax, initialvalue)
        # pre-calculate offsets for neighbour cells
        self._neighbour_index_offsets = tuple(offset.value.x + self.width * offset.value.y for offset in Direction)

    def neighbours(self, point):
        base = self.xy_to_index(point)
        return Neighbours(*[self._array[base + offset] for offset in self._neighbour_index_offsets])


def bounding_box(elves):
    xmin, ymin = elves[0].pos
    xmax, ymax = elves[0].pos
    for elf in elves:
        x, y = elf.pos
        xmin = min(x, xmin)
        xmax = max(x, xmax)
        ymin = min(y, ymin)
        ymax = max(y, ymax)
    return Point(xmin, ymin), Point(xmax, ymax)


def parse(stream):
    elves = []
    for y, line in enumerate(stream):
        for x, c in enumerate(line):
            if c == chr(Item.ELF):
                elves.append(Elf(Point(x, y)))
    return elves


Scan = namedtuple('Scan', 'check_fn propose')
scan_list = (
    Scan(Neighbours.can_move_n, Direction.N),
    Scan(Neighbours.can_move_s, Direction.S),
    Scan(Neighbours.can_move_w, Direction.W),
    Scan(Neighbours.can_move_e, Direction.E)
)


def diffusion(elves, max_cycles):

    # must do this inside the function, otherwise it doesn't reset between invocations
    scan_cycle = cycle((
        (scan_list[0], scan_list[1], scan_list[2], scan_list[3]),
        (scan_list[1], scan_list[2], scan_list[3], scan_list[0]),
        (scan_list[2], scan_list[3], scan_list[0], scan_list[1]),
        (scan_list[3], scan_list[0], scan_list[1], scan_list[2]),
    ))

    # create initial grid and mark elf positions
    top_left, bottom_right = bounding_box(elves)
    grid = Grid('B', top_left.x - 1, bottom_right.x + 1, top_left.y - 1, bottom_right.y + 1, Item.SPACE)
    for elf in elves:
        grid[elf.pos] = Item.ELF
    #print(f'\n== Initial State ==\n{grid.as_chars()}')

    for cycle_num in range(1, max_cycles + 1):
        # rotate order of scans
        scans = next(scan_cycle)

        # create movement proposals 
        neighbours_exist = False
        proposal_dict = {}
        blocked_proposals = set()
        for elf in elves:
            neighbours = grid.neighbours(elf.pos)
            num_neighbours = neighbours.count(Item.ELF)
            if num_neighbours:
                neighbours_exist = True
                for scan in scans:
                    if scan.check_fn(neighbours):
                        # propose new coords
                        proposal = elf.pos + scan.propose.value

                        if proposal in proposal_dict:
                            # these coords have already been proposed
                            blocked_proposals.add(proposal)
                        else:
                            proposal_dict[proposal] = elf
                        break

        # check for completion
        if neighbours_exist == False:
            break
            

        # evaluate and execute proposals
        for proposal, proposer in proposal_dict.items():
            if proposal not in blocked_proposals:
                proposer.pos = proposal

         # create suitably-sized grid and mark elf positions
        del(grid)
        top_left, bottom_right = bounding_box(elves)
        grid = Grid('B', top_left.x - 1, bottom_right.x + 1, top_left.y - 1, bottom_right.y + 1, Item.SPACE)
        for elf in elves:
            grid[elf.pos] = Item.ELF

        # display board
        #print(f'\n== End of Round {cycle_num} ==\n{grid.as_chars()}')

    return grid, cycle_num
    

def part1(stream):
    elves = parse(stream)
    grid, cycle_num = diffusion(elves, max_cycles=10)

    # count blank elements excluding border
    for x in range(grid.xmin, grid.xmax + 1):
        grid[x, grid.ymin] = Item.NONE
        grid[x, grid.ymax] = Item.NONE
    for y in range(grid.ymin, grid.ymax + 1):
        grid[grid.xmin, y] = Item.NONE
        grid[grid.xmax, y] = Item.NONE

    return grid._array.count(Item.SPACE)


def part2(stream):
    elves = parse(stream)
    grid, cycle_num = diffusion(elves, max_cycles=1_000_000)

    return cycle_num


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 110, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 20, result


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