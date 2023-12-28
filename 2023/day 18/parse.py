from grid import Grid
from enum import Enum
from dataclasses import dataclass


class Dir(Enum):
    U = (0, 1)
    R = (1, 0)
    D = (0, -1)
    L = (-1, 0)


def parse(stream):
    stream.seek(0)

    # get the extent of the map
    x = 0
    y = 0
    xmax = xmin = 0
    ymax = ymin = 0

    for rawline in stream:
        line = rawline.strip()

        code, countStr, colourStr = line.split()
        dir = Dir[code]
        count = int(countStr)

        dx, dy = dir.value
        x += dx * count
        y += dy * count

        xmax = max(x, xmax)
        xmin = min(x, xmin)

        ymax = max(y, ymax)
        ymin = min(y, ymin)

    # add a border
    xmin -= 1
    xmax += 1
    ymin -= 1
    ymax += 1

    width = xmax - xmin + 1
    height = ymax - ymin + 1

    xStart = -xmin
    yStart = -ymin

    # create the grid
    stream.seek(0)
    grid = Grid(width, height, height * ['.' * width])
    x, y = xStart, yStart

    for rawline in stream:
        line = rawline.strip()

        code, countStr, colourStr = line.split()
        dir = Dir[code]
        count = int(countStr)

        dx, dy = dir.value

        for _ in range(count):
            grid[x, y] = '#'
            x += dx
            y += dy

    return grid


@dataclass
class Point:
    x: int
    y: int
    isEdge: bool

    def __str__(self):
        if self.isEdge:
            return f'({self.x}, {self.y})*'
        else:
            return f'({self.x}, {self.y})'
                

def isEdge(prevDir: Dir, dir: Dir) -> bool:
    # whether this vertex takes us across the boundary when moving sideways
    if prevDir is Dir.U:
        assert dir is Dir.L or dir is Dir.R
        return True
    elif prevDir is Dir.D:
        assert dir is Dir.L or dir is Dir.R
        return False
    elif prevDir is Dir.R or prevDir is Dir.L:
        assert dir is Dir.U or dir is Dir.D
        if dir is dir.U:
            return False
        elif dir is dir.D:
            return True
    return False


def parse2(stream):
    stream.seek(0)

    # extract vertices

    vertices = []
    x = 0
    y = 0
    prevDir = None

    for rawline in stream:
        line = rawline.strip()

        _, _, colourStr = line.split()

        # decode colourStr
        colourStr = colourStr.strip('()')
        assert colourStr[0] == '#'
        colourStr = colourStr.lstrip('#')
        count = int(colourStr[:5], 16)
        dir = [Dir.R, Dir.D, Dir.L, Dir.U][int(colourStr[5])]

        vertices.append(Point(x, y, isEdge(prevDir, dir)))

        dx, dy = dir.value
        x += dx * count
        y += dy * count
        
        if prevDir is None:
            firstDir = dir
        prevDir = dir

    # check the path is closed
    assert (x, y) == (0, 0)

    # add the final vertex
    vertices.append(Point(x, y, isEdge(dir, firstDir)))

    # correct the 'isEdge' flag on the first vertex
    vertices[0].isEdge = isEdge(dir, firstDir)


    return vertices