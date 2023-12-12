from array import array

class Grid:
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