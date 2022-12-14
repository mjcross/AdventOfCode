from array import array
from itertools import cycle

class Array2D:
    def __init__(self, typecode='i', xmin=0, xmax=0, ymin=0, ymax=0, initialvalue=0):
        assert xmax >= xmin and ymax >= ymin
        self.typecode = typecode
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.width = 1 + xmax - xmin
        self.height = 1 + ymax - ymin
        self._array = array(typecode, [initialvalue] * self.width * self.height)

    def __len__(self):
        return len(self._array)

    def xy_to_index(self, xy):
        x, y = xy
        if x < self.xmin or x > self.xmax or y < self.ymin or y > self.ymax:
            raise IndexError()
        else:
            x_offset = x - self.xmin
            y_offset = y - self.ymin
            return x_offset + y_offset * self.width

    def __getitem__(self, index):
        return self._array[self.xy_to_index(index)]
        
    def __setitem__(self, index, value):
        self._array[self.xy_to_index(index)] = value

    def index_to_xy(self, index):
        x_offset = index % self.width
        y_offset = index // self.width
        return (x_offset + self.xmin, y_offset + self.ymin)

    def __repr__(self):
        repr = (
            f'Array2D(typecode={self.typecode}, '
            f'xmin={self.xmin}, xmax={self.xmax}, ymin={self.ymin}, ymax{self.ymax})'
        )

        for rowstart in range(0, len(self._array), self.width):
            repr += f'\n{self._array[rowstart: rowstart + self.width].tolist()}'

        return repr

    
def main():
    a2d = Array2D('B', 5, 9, 2, 5)
    a2d[6, 3] = 1
    assert a2d[6, 3] == 1
    print(a2d)

if __name__ == '__main__':
    main()