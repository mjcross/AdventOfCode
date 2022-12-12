from array import array

class Map:
    def __init__(self):
        self.height = array('B')
        self.nrows = 0
        self.ncols = 0

    def __repr__(self):
        repr = ''
        for rowstart in range(0, len(self.height), self.ncols):
            for height in self.height[rowstart: rowstart + self.ncols]:
                repr += chr(height)
            repr += '\t'
            if self.visited:
                for visited in self.visited[rowstart: rowstart + self.ncols]:
                    if visited:
                        repr += 'x'
                    else:
                        repr += '-'
            repr += '\n'
        return repr

    def fromstream(self, stream): 
        for line in stream:
            row = [ord(c) for c in line.strip()]
            self.nrows += 1
            self.height.extend(row)
        self.ncols = len(row)

        self.startpositions = [self.height.index(ord('S'))]
        for startpos in self.startpositions:
            self.height[startpos] = ord('a')

        self.endpos = self.height.index(ord('E'))
        self.height[self.endpos] = ord('z')

    def bestpathlen(self):
        nrows = self.nrows
        ncols = self.ncols
        self.visited = array('B', [False for _ in self.height])
        points = self.startpositions
        for point in points:
            self.visited[point] = True
        pathlen = 0
        while points:
            pathlen += 1
            newpoints = []
            for point in points:
                offsets = []
                if point % ncols > 0:
                    offsets.append(-1)
                if point % ncols < (ncols - 1):
                    offsets.append(1)
                if point + ncols < len(self.height):
                    offsets.append(ncols)
                if point - ncols >= 0:
                    offsets.append(-ncols)
                for candidate in [point + offset for offset in offsets]:
                    if not self.visited[candidate] and self.height[candidate] <= 1 + self.height[point]:
                        self.visited[candidate] = True
                        newpoints.append(candidate)
                        if candidate == self.endpos:
                            return pathlen
            points = newpoints
        return None

def part1(stream):
    map = Map()
    map.fromstream(stream)
    return map.bestpathlen()


def part2(stream):
    map = Map()
    map.fromstream(stream)
    map.startpositions = [position for position, height in enumerate(map.height) if height == ord('a')]
    return map.bestpathlen()


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream)
        assert example1 == 31, example1

    with open('example.txt') as stream:
        example2 = part2(stream)
        assert example2 == 29, example2


def main():
    checkexamples()

    with open('input.txt') as stream:
        print('part1', part1(stream))

    with open('input.txt') as stream:
        print('part2', part2(stream))


if __name__ == '__main__':
    main()