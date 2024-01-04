from dataclasses import dataclass, field
from array import array


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __str__(self):
        return f'{self.x}, {self.y}, {self.z}'
    
@dataclass
class Brick:
    index: int
    min: Point
    max: Point
    supports: set = field(default_factory=set)
    supportedBy: set = field(default_factory=set)

    def __post_init__(self):
        # check the ranges are the right way round
        assert self.max.x >= self.min.x >= 0
        assert self.max.y >= self.min.y >= 0
        assert self.max.z >= self.min.z > 0     # all bricks must have z >= 1

    def getPoints(self):
        points = []
        for x in range(self.min.x, self.max.x + 1):
            for y in range(self.min.y, self.max.y + 1):
                for z in range(self.min.z, self.max.z + 1):
                   points.append(Point(x, y, z))
        return points 


@dataclass
class Grid3D:
    width: int
    height: int
    _array: array

    def __getitem__(self, coord):
        x, y, z = coord
        return self._array[x + self.width * (y + self.height * z)]

    def __setitem__(self, coord, value):
        x, y, z = coord
        self._array[x + self.width * (y + self.height * z)] = value

    def debug(self):
        for z in range(numZ):
            for y in range(numY):
                for x in range(numX):
                    print(grid[x, y, z], end=' ')
                print()
            print('------')
        print()


def part1(stream):

    EMPTY = -2
    GROUND = -1

    # create bricks from stream
    bricks = []
    xmax = 0
    ymax = 0
    zmax = 0
    for index, rawline in enumerate(stream):
        line = rawline.strip()

        point1Str, point2Str = line.split('~')

        x, y, z = point1Str.split(',')
        point1 = Point(int(x), int(y), int(z))

        x, y, z = point2Str.split(',')
        point2 = Point(int(x), int(y), int(z))

        bricks.append(Brick(index, point1, point2))
    
    # plot bricks on 3D grid
    numX = 1 + max([brick.max.x for brick in bricks])
    numY = 1 + max([brick.max.y for brick in bricks])
    numZ = 1 + max([brick.max.z for brick in bricks])

    grid = Grid3D(numX, numY, array('i', numX * numY * numZ * [EMPTY]))

    for brick in bricks:
        for x in range(brick.min.x, brick.max.x + 1):
            for y in range(brick.min.y, brick.max.y + 1):
                for z in range(brick.min.z, brick.max.z + 1):
                    grid[x, y, z] = brick.index

    # add ground surface at z=0
    for x in range(numX):
        for y in range(numY):
            grid[x, y, 0] = GROUND

    # let bricks settle into place
    somethingMoved = True
    while somethingMoved:
        somethingMoved = False
        for brick in bricks:
            for point in brick.getPoints():
                if grid[point.x, point.y, brick.min.z - 1] != EMPTY:
                    break
            else:
                somethingMoved = True
                # move the brick down one place
                for point in brick.getPoints():
                    grid[point.x, point.y, point.z] = EMPTY
                brick.min.z -= 1
                brick.max.z -= 1
                for point in brick.getPoints():
                    grid[point.x, point.y, point.z] = brick.index

    # determine how the bricks support each other
    for brick in bricks:
        for point in brick.getPoints():
            index = grid[point.x, point.y, brick.min.z - 1]
            if index != EMPTY:
                brick.supportedBy.add(index)
                if index != GROUND:
                    bricks[index].supports.add(brick.index)

    # count the bricks that can be safely removed
    safeBricks = set()
    for brick in bricks:
        if len(brick.supports) == 0:
            safeBricks.add(brick.index)
        if len(brick.supportedBy) > 1:
            for index in brick.supportedBy:
                safeBricks.add(index)
    return len(safeBricks)


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
    #    assert result == 'xxxxx', result

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