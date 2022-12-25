from array import array
import sys
sys.setrecursionlimit(8000)    # 3D recursive fill needs a lot of stack

offsets = (
    (-1,  0,  0),
    (+1,  0,  0),
    ( 0, -1,  0),
    ( 0, +1,  0),
    ( 0,  0, -1),
    ( 0,  0, +1)
)

ROCK = ord('#')
AIR = ord('.')
WATER = ord('-')


class Array3D:
    def __init__(self, typecode, xmin, xmax, ymin, ymax, zmin, zmax, initialvalue=0):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        self._sizex = xmax - xmin
        self._sizey = ymax - ymin
        self._sizez = zmax - zmin
        self._array = array(typecode, self._sizex * self._sizey * self._sizez * [initialvalue])

    def __repr__(self):
        repr = ''
        for z in range(self.zmin, self.zmax):
            dz = z - self.zmin
            for y in range(self.ymin, self.ymax):
                dy = y - self.ymin
                rowstart = self._sizex * (y + dz * self._sizey)
                row = self._array[rowstart: rowstart + self._sizex]
                repr += ''.join(map(chr, row))
                repr += '\n'
            repr += '\n'
        return repr

    def __getitem__(self, tuple_xyz):
        x, y, z = tuple_xyz
        dx = x - self.xmin
        dy = y - self.ymin
        dz = z - self.zmin
        return self._array[dx + self._sizex * (y + dz * self._sizey)]

    def __setitem__(self, tuple_xyz, value):
        x, y, z = tuple_xyz
        dx = x - self.xmin
        dy = y - self.ymin
        dz = z - self.zmin
        self._array[dx + self._sizex * (y + dz * self._sizey)] = value


def parse(stream):
    cube = {}
    firsttime = True
    for line in stream:
        x, y, z = map(int, line.split(','))
        if firsttime:
            xmin = xmax = x
            ymin = ymax = y
            zmin = zmax = z
            firsttime = False
        else:
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
            zmin = min(zmin, z)
            zmax = max(zmax, z)
        cube[x, y, z] = 1
    return cube, xmin, xmax, ymin, ymax, zmin, zmax


def part1(stream):
    pixeldict, xmin, xmax, ymin, ymax, zmin, zmax = parse(stream)
    sa_tot = 0
    for x, y, z in pixeldict.keys():
        sa_this = 6
        for dx, dy, dz in offsets:
            sa_this -= pixeldict.get((x + dx, y + dy, z + dz), 0)
        sa_tot += sa_this
    return sa_tot


def flood(grid, x, y, z, sa):
    grid[(x, y, z)] = WATER
    for dx, dy, dz in offsets:
        newx = x + dx
        newy = y + dy
        newz = z + dz
        if (    newx >= grid.xmin
                and newx < grid.xmax 
                and newy >= grid.ymin 
                and newy < grid.ymax 
                and newz >= grid.zmin 
                and newz < grid.zmax):
            pixel = grid[(newx, newy, newz)]
            if pixel == AIR:
                sa = flood(grid, newx, newy, newz, sa)
            elif pixel == ROCK:
                sa += 1
    return sa


def part2(stream):
    pixeldict, xmin, xmax, ymin, ymax, zmin, zmax = parse(stream)

    # expand bounding box to give a gap all round
    xmin -= 1
    xmax += 1
    ymin -= 1
    ymax += 1
    zmin -= 1
    zmax += 1
    
    grid = Array3D('B', xmin, xmax + 1, ymin, ymax + 1, zmin, zmax + 1, AIR)

    for coord in pixeldict.keys():
        grid[coord] = ROCK

    # recursively fill airspace with water; count how may times we touched rock
    sa = flood(grid, xmin, ymin, zmin, 0)
    #print(grid)
    return sa


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: surface area {result}')
        assert result == 64, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: external surface area {result}')
        assert result == 58, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print('part1: surface area', result)

    with open('input.txt') as stream:
        result = part2(stream)
        print('part2: external surface area', result)


if __name__ == '__main__':
    main()