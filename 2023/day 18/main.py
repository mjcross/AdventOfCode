from parse import parse, parse2, Point
from itertools import pairwise
from dataclasses import dataclass
from typing import Self

def part1(stream):
    grid = parse(stream)
    grid.floodFill(0, 0, '.', '|')
    return grid._array.count(ord('.')) + grid._array.count(ord('#'))


@dataclass
class Line:
    a: Point
    b: Point

    def __post_init__(self):
        # sort ends
        if self.a.x > self.b.x or self.a.y > self.b.y:
            self.a, self.b = self.b, self.a

    def __len__(self):
        return self.b.x - self.a.x + self.b.y - self.a.y
    
    def slice(self, y: int) -> list[int]:
        if self.a.y == y and self.b.y == y:
            return self
        elif self.a.y < y < self.b.y:
            assert self.a.x == self.b.x
            return Line(Point(self.a.x, y, True), Point(self.a.x, y, False))
        else:
            return None
        
    def __gt__(self, other):
        return self.a.x > other.b.x


def slice(lines: list[Line], y: int) -> list[Line]:
    """
    Returns a left-to-right ordered list of the grid defined by line segments
    `lines`, for a horizontal slice at ordinate `y`.
    """
    return sorted([l.slice(y) for l in lines if l.slice(y) is not None])


def sliceVolume(lines: list[Line], y: int) -> int:
    """
    Returns the volume of the surrounding trench and infill, for a horizontal 
    slice through the grid at ordinate `y`.
    """
    isInside = False
    x = 0
    volume = 0
    for line in slice(lines, y):
        if isInside:
            volume += line.a.x - x   # if we are inside, then include the gap between lines
        x = line.a.x
        if line.a.isEdge:
            isInside = not(isInside)
        if line.b.isEdge:
            isInside = not(isInside)
        x += len(line) + 1
        volume += len(line) + 1  # always include the volume of the trench
    assert isInside is False 
    return volume


def part2(stream):
    # extract the vertices, marking them if they are '7' or 'F' turns
    vertices = parse2(stream)

    # create line segments from the vertices
    lines = [Line(v1, v2) for v1, v2 in pairwise(vertices)]

    # create a sorted, de-duplicated list of the y ordinates that have vertices
    yOrd = sorted(list(set([vertex.y for vertex in vertices])), reverse=True)

    vTot = 0
    y = yOrd[-1] + 1    # ensure that deltaY is 1 for the first step
    while yOrd:
        # iterate upwards through the y ordinates containing horizontal line segments
        yPrev = y
        y = yOrd.pop()
        deltaY = y - yPrev

        if deltaY > 1:
            # we skipped some 'plain' rows that contain no horizontal line segments and
            # must therefore be identical
            vTot += (deltaY - 1) * sliceVolume(lines, yPrev + 1)

        # calculate and accumulate the volume of this slice
        vTot += sliceVolume(lines, y)

    return vTot





def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 62, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 952408144115, result


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