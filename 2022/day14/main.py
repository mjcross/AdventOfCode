from array import array
from collections import namedtuple
from enum import Enum
Point = namedtuple('Point', 'x y')

class Tile(Enum):
    Air = ord('.')
    Rock = ord('#')
    Sand = ord('o')

class Array2D():
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self._array = array()
    


def parse(stream):
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
    


def part1(stream):
    rocks = parse(stream)


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream)
        assert example1 == 'xxxxx', example1

    #with open('example.txt') as stream:
    #    example2 = part2(stream)
    #    assert example2 == 'xxxxx', example2


def main():
    checkexamples()

    #with open('input.txt') as stream:
    #    print('part1', part1(stream))

    #with open('input.txt') as stream:
    #    print('part2', part2(stream))


if __name__ == '__main__':
    main()