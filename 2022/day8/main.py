from array import array

class Grid:
    def __init__(self):
        self.data = array('B')
        self.nrows = 0
        self.ncols = 0

    def rc(self, row, col):
        return self.data[row * self.ncols + col]


def gridfromfile(file):
    grid = Grid()
    for line in file:
        grid.data.extend(map(int, line.rstrip()))
        grid.nrows += 1
    grid.ncols = len(grid.data) // grid.nrows
    assert grid.ncols * grid.nrows == len(grid.data)
    return grid


def updatevisibility(height, visibility, indices):
    highest = -1
    for index in indices:
        if height[index] > highest:
            highest = height[index]
            visibility[index] = 1


def part1(grid):
    visibility = array('B', [0] * len(grid.data))
    for rownum in range(grid.nrows):
        rowstart = rownum * grid.ncols
        rowrange = range(rowstart, rowstart + grid.ncols)
        updatevisibility(grid.data, visibility, rowrange)
        updatevisibility(grid.data, visibility, reversed(rowrange))

    for colnum in range(grid.ncols):
        colrange = range(colnum, colnum + grid.nrows * grid.ncols, grid.ncols)
        updatevisibility(grid.data, visibility, colrange)
        updatevisibility(grid.data, visibility, reversed(colrange))

    return sum(visibility)         
    

def part2(grid):
    bestscore = 0
    for houserownum in range(grid.nrows):
        for housecolnum in range(grid.ncols):
            househeight = grid.rc(houserownum, housecolnum)

            rightview = 0
            highest = 0
            for colnum in range(housecolnum + 1, grid.ncols):
                rightview += 1
                height = grid.rc(houserownum, colnum)
                if height >= househeight:
                    break

            leftview = 0
            highest = 0
            for colnum in reversed(range(0, housecolnum)):
                leftview += 1
                height = grid.rc(houserownum, colnum)
                if height >= househeight:
                    break

            downview = 0
            for rownum in range(houserownum + 1, grid.nrows):
                downview += 1
                height = grid.rc(rownum, housecolnum)
                if height >= househeight:
                    break

            upview = 0
            for rownum in reversed(range(0, houserownum)):
                upview += 1
                height = grid.rc(rownum, housecolnum)
                if height >= househeight:
                    break

            score = upview * leftview * rightview * downview
            bestscore = max(score, bestscore)

    return bestscore


def checkexamples():
    with open('example.txt') as file:
        grid = gridfromfile(file)
        assert part1(grid) == 21
        print('example 1 OK')
        assert part2(grid) == 8
        print('example 2 OK')


def main():
    checkexamples()

    with open('input.txt') as infile:
        grid = gridfromfile(infile)
        print(part1(grid))
        print(part2(grid))
    

if __name__ == '__main__':
    main()