from array import array

class Grid:
    """Efficient storage of 2D character data using an Array.
       Instances are intended to be easy to initialise from
       an iterable (e.g. text file data)."""
    def indexToCoord(self, index):
        x = index % self.width
        y = (self.height - 1) - index // self.width
        return x, y

    def coordToIndex(self, coord):
        x, y = coord
        if x < 0 or x >= self.width:
            raise ValueError
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

    def __getitem__(self, coord):
        return chr(self._array[self.coordToIndex(coord)])

    def __setitem__(self, coord, value):
        self._array[self.coordToIndex(coord)] = ord(value)

    def __str__(self):
        return '\n'.join(
            [''.join(list(map(chr, self._array[y * self.width: (y+1) * self.width])))
            for y in range(self.height)])


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