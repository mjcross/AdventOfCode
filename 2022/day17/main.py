from itertools import cycle
from array import array
from utils.findall import findall
from utils.listdelta import delta

EMPTY = ord('.')

class Sprite:
    def __init__(self, rows, boardwidth, chr, x=2, y=1):
        self.boardwidth = boardwidth
        self.chr = chr
        self._x = x
        self._y = y
        self._width = 0
        self._height = 0
        self._id = ord(chr)
        self._base = x + y * boardwidth
        self._offsets = array('B')
        for pixel_y, row in enumerate(reversed(rows)):
            for pixel_x, pixel_value in enumerate(row):
                if pixel_value != ' ':
                    self._width = max(self._width, pixel_x)
                    self._height = max(self._height, pixel_y)
                    self._offsets.append(pixel_x + pixel_y * boardwidth)
        self._width += 1

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._base = value + self._y * self.boardwidth 

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._base = self._x + value * self.boardwidth

    @property
    def ymax(self):
        return self._y + self._height

    def move_by(self, dx, dy, board):
        if self.x == 0 and dx < 0:
            return False

        if self.x + self._width == self.boardwidth and dx > 0:
            return False

        new_base = self._base + dx + dy * self.boardwidth

        for offset in self._offsets:
            if board[new_base + offset] != EMPTY:
                return False
        
        self._base = new_base
        self._x += dx
        self._y += dy
        return True

    def draw(self, board):
        for offset in self._offsets:
            board[self._base + offset] = self._id


pieces = (
    Sprite(rows=['####'], boardwidth=7, chr='1'),
    Sprite(rows=[' # ', '###', ' # '], boardwidth=7, chr='2'),
    Sprite(rows=['  #', '  #', '###'], boardwidth=7, chr='3'),
    Sprite(rows=['#', '#', '#', '#'], boardwidth=7, chr='4'),
    Sprite(rows=['##', '##'], boardwidth=7, chr='5')
)


def parse(stream):
    dx = []
    for character in stream.readline().strip():
        if character == '<':
            dx.append(-1)
        elif character == '>':
            dx.append(+1)
        else:
            raise ValueError(f'unrecognised character in input: "{character}"')
    return dx


def showboard(board, width, from_row=0, to_row=5):
    for rowstart in reversed(range(width * from_row, width * (1 + to_row), width)):
        print(''.join(list(map(chr, board[rowstart: rowstart + width]))))


def simulate(stream, num_rocks, board_height):
    piece_seq = cycle(pieces)
    dx_seq = cycle(parse(stream))

    board = array('B', board_height * 7 * [EMPTY])
    board[0: 7] = array('B', 7 * [ord('#')])

    height =  [0]
    ymax = 0
    for _ in range(num_rocks):
        # initialise next piece
        piece = next(piece_seq)
        piece.x = 2
        piece.y = height[-1] + 4
        # let it fall
        while True:
            # move sideways
            piece.move_by(next(dx_seq), 0, board)
            # move down
            if piece.move_by(0, -1, board) == False:
                # obstructed
                piece.draw(board)
                ymax = max(piece.ymax, ymax)
                height.append(ymax)
                break
    return board, height


def part1(stream, num_rocks, board_height):
    board, tower_height = simulate(stream, num_rocks, board_height)
    return tower_height[-1]


def part2(stream, sample_size, targetrocks):
    # look for repeating patterns
    # create a nice big tower
    num_rocks = 5 * sample_size
    board, height = simulate(stream, num_rocks=num_rocks, board_height=int(1.6 * num_rocks))

    # look for repeats in the pattern of height increases
    heightchange = array('B', delta(height)).tobytes()
    middlerock = num_rocks // 2
    sample = heightchange[middlerock: middlerock + sample_size]
    occurrences = findall(needle=sample, haystack=heightchange)
    deltas = list(delta(occurrences))

    rockstart = occurrences[0]                  # number of rocks dropped when the pattern first appears
    rockperiod = sum(deltas) // len(deltas)     # number rocks required to make the pattern re-occur
    #print(f'height increase pattern appears after {rockstart} rocks and then repeats every {rockperiod} rocks')

    heightstart = height[rockstart]
    heightchange = height[rockstart + rockperiod] - heightstart
    #print(f'height when pattern appears is {heightstart}, and it increases {heightchange} every cycle')

    numcycles = (targetrocks - rockstart) // rockperiod
    heightaftercycles = heightstart + heightchange * numcycles
    numrocks = rockstart + numcycles * rockperiod
    #print(f'we expect the height after {numcycles} cycles to be {heightaftercycles}, having dropped {numrocks} rocks')

    extrarocks = targetrocks - numrocks
    heightincrease = height[rockstart + extrarocks] - height[rockstart]
    #print(f'we now need to drop {extrarocks} more rocks, which we expect to increase the height by {heightincrease}')

    heightaftertargetrocks = heightaftercycles + heightincrease
    #print(f'taking the height after {targetrocks} rocks to {heightaftertargetrocks}')

    return heightaftertargetrocks



def checkexamples():
    with open('example.txt', 'r') as stream:
        tower_height = part1(stream, num_rocks=2022, board_height = 3075)
        print('example1: tower height', tower_height)
        assert tower_height == 3068, tower_height

    with open('example.txt') as stream:
        tower_height = part2(stream, sample_size=250, targetrocks=1_000_000_000_000)
        print('example2: tower height', tower_height)
        assert tower_height == 1514285714288, tower_height


def main():
    checkexamples()

    with open('input.txt') as stream:
        tower_height = part1(stream, num_rocks=2022, board_height = 3200)
        print('part1: tower height', tower_height)

    with open('input.txt') as stream:
        tower_height = part2(stream, sample_size=1_000, targetrocks=1_000_000_000_000)
        print('part2: tower height', tower_height)


if __name__ == '__main__':
    main()