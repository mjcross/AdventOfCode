from parse import parse, Brick
from grid import ListGrid
from dataclasses import dataclass


@dataclass
class Point2D:
    x: int
    y: int

    def __str__(self):
        return f'{self.x}, {self.y}'

def part1(stream):
    bricks = parse(stream)

    xMax = max([brick.max.x for brick in bricks])
    yMax = max([brick.max.y for brick in bricks])
    zMax = max([brick.min.z for brick in bricks])
    ground = Brick(None, (0, 0, 0), (xMax, yMax, 0))
    xyBricks = ListGrid(xMax + 1, yMax + 1, (xMax + 1)*(yMax + 1)*[ground])

    for z in range(zMax + 1):

        for brick in bricks:
            if brick.min.z == z:
                brick.supportedByIndices = {None}

                # find highest point(s) under brick
                zMax = 0
                for x in range(brick.min.x, brick.max.x + 1):
                    for y in range(brick.min.y, brick.max.y + 1):
                        xyBrick = xyBricks[x, y]
                        if xyBrick.max.z > zMax:
                            zMax = xyBrick.max.z
                            brick.supportedByIndices = {xyBrick.index}
                        elif xyBrick.max.z == zMax:
                            brick.supportedByIndices.add(xyBrick.index)

                # place brick
                deltaZ = zMax - brick.min.z + 1
                brick.min.z += deltaZ
                brick.max.z += deltaZ

                # update highest points on grid
                for x in range(brick.min.x, brick.max.x + 1):
                    for y in range(brick.min.y, brick.max.y + 1):
                        xyBricks[x, y] = brick

                # update supporing bricks to show that they support this brick
                for i in brick.supportedByIndices:
                    if i is not None:
                        bricks[i].supportsIndices.add(brick.index)

                print('placed:', brick)

    print()
    for brick in bricks:
        print('Brick', brick.index, 'supports', brick.supportsIndices, 'supportedBy', brick.supportedByIndices)

    removeable = set()
    for brick in bricks:
        if len(brick.supportedByIndices) > 1:
            removeable.update(brick.supportedByIndices)
        if len(brick.supportsIndices) == 0:
            removeable.add(brick.index)

    print()
    print('removeable:', removeable)

    return(len(removeable))


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 5, result

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