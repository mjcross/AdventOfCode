from array import array

def gridFromstream(stream):
    # find dimensions of grid
    width = len(stream.readline().strip('\n'))

    height = 1
    while stream.readline():
        height += 1

    # rewind stream and initialise grid
    stream.seek(0)
    return Grid(width, height, [line.strip('\n') for line in stream])


class Grid:
    """
    Efficient storage of 2D character data using an Array.
    To initialise from a stream use 'gridFromStream()', above.
    """
    def indexToCoord(self, index):
        x = index % self.width
        y = (self.height - 1) - index // self.width
        return x, y

    def coordToIndex(self, coord):
        x, y = coord
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError
        return x + self.width * (self.height - 1 - y)
    
    def find(self, c):
        return self.indexToCoord(self._array.index(ord(c)))
    
    def findAll(self, c):
        start = 0
        found = []
        try:
            while True:
                i = self._array.index(ord(c), start)
                found.append(self.indexToCoord(i))
                start = i + 1
        except ValueError:
            return found

    def __init__(self, width, height, initialiser=None):
        self.width = width
        self.height = height
        if initialiser is None:
            self._array = array('B', [ord(' ')] * height * width,)
        else:
            self._array = array('B', map(ord, ''.join(initialiser)))

    def __hash__(self):
        return hash(tuple(self._array))

    def __getitem__(self, coord):
        return chr(self._array[self.coordToIndex(coord)])

    def __setitem__(self, coord, value):
        self._array[self.coordToIndex(coord)] = ord(value)

    def __str__(self):
        return '\n'.join(
            [''.join(list(map(chr, self._array[y * self.width: (y+1) * self.width])))
            for y in range(self.height)]) + '\n'
    
    def floodFill(self, x, y, empty='.', fill=' '):
    
        def isEmpty(x, y, empty, grid):
            try:
                if grid[x, y] == empty:
                    return True
                return False
            except IndexError:
                return False
              
        coords = [(x, y)]
        while coords:
            x0, y = coords.pop()

            # go right
            x = x0
            prevEmptyAbove = False
            prevEmptyBelow = False
            while isEmpty(x, y, empty, self):
                self[x, y] = fill

                # check above
                if isEmpty(x, y + 1, empty, self):
                    if not prevEmptyAbove:
                        coords.append((x, y + 1))
                    prevEmptyAbove = True
                else:
                    prevEmptyAbove = False

                # check below
                if isEmpty(x, y - 1, empty, self):
                    if not prevEmptyBelow:
                        coords.append((x, y - 1))
                    prevEmptyBelow = True
                else:
                    prevEmptyBelow = False

                x += 1

            # go left
            x = x0 - 1
            prevEmptyAbove = False
            prevEmptyBelow = False
            while isEmpty(x, y, empty, self):
                self[x, y] = fill

                # check above
                if isEmpty(x, y + 1, empty, self):
                    if not prevEmptyAbove:
                        coords.append((x, y + 1))
                    prevEmptyAbove = True
                else:
                    prevEmptyAbove = False

                # check below
                if isEmpty(x, y - 1, empty, self):
                    if not prevEmptyBelow:
                        coords.append((x, y - 1))
                    prevEmptyBelow = True
                else:
                    prevEmptyBelow = False

                x -= 1


class IntGrid(Grid):
    """
    A subclass of grid where the element accesses use ints
    instead of chars.
    """
    def __init__(self, width, height, initialiser=None):
        self.width = width
        self.height = height
        if initialiser is None:
            self._array = array('I', [0] * height * width,)
        else:
            self._array = array('I', map(int, ''.join(initialiser)))

    def __getitem__(self, coord):
        return self._array[self.coordToIndex(coord)]

    def __setitem__(self, coord, value):
        self._array[self.coordToIndex(coord)] = value

    def find(self, c):
        return self.indexToCoord(self._array.index(c))
    
    def findAll(self, c):
        start = 0
        found = []
        try:
            while True:
                i = self._array.index(c, start)
                found.append(self.indexToCoord(i))
                start = i + 1
        except ValueError:
            return found
        
    def __str__(self):
        m = max(self._array)
        l = len(str(m))
        s = ''
        for y in reversed(range(self.height)):
            row = (', ').join([f'{self[x, y]:{l}}' for x in range(self.width)])
            s += row + '\n'
        return s

class ListGrid(Grid):
    """A subclass of Grid that uses a List as the underlying
       storage instead of an Array. It's less memory-efficient
       but it allows the elements to be more complex types
       such as objects."""
    def find(self, c):
        return self.indexToCoord(self._array.index(c))

    def __init__(self, width, height, initialiser=None):
        self.width = width
        self.height = height
        if initialiser is None:
            self._array = list(None * height * width)
        else:
            self._array = list(initialiser)

    def __getitem__(self, coord):
        return self._array[self.coordToIndex(coord)]

    def __setitem__(self, coord, value):
        self._array[self.coordToIndex(coord)] = value
    

def main():
    # simple tests
    grid = Grid(3, 4, ['...', '...', '...', '...'])
    for coord in [(0, 3), (2, 1), (2, 0)]:
        grid[coord] = '*'
    assert grid[2, 1] == '*'
    print(grid)
    assert grid.find('*') == (0, 3)
    assert grid.findAll('*') == [(0, 3), (2, 1), (2, 0)]
    print('tests OK')

if __name__ == '__main__':
    main()