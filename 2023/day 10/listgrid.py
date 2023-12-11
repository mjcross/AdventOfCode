from grid import Grid

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
    grid = Grid(3, 4, ['abc', 'def', 'ghi', 'jkl'])
    grid[1, 2] = '*'
    assert grid[1, 2] == '*'
    print(grid)
    assert grid.find('*') == (1, 2)
    print('tests OK')

if __name__ == '__main__':
    main()