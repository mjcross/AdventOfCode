class Board:
    def __init__(self, boardindex):
        self.numbers = []
        self.boardindex = boardindex
        self.iscomplete = False

    def __repr__(self):
        repr = f'Board {1 + self.boardindex} (index {self.boardindex})'
        for row in range(5):
            repr += '\n\t\t'
            for col in range(5):
                num = self.rc(row, col)
                if num >= 0:
                    repr += f'{num:2d}  '
                elif num == -1:
                    repr += '--  '
                else:
                    repr += '==  '
        return repr + '\n'

    def rc(self, row, col):
        return self.numbers[col + row * 5]

    def fromstream(self, stream):
        for row in range(5):
            self.numbers += map(int, stream.readline().split())

    def draw(self, num):
        if not self.iscomplete:
            try:
                i = self.numbers.index(num)
                row = i // 5
                col = i % 5
                self.numbers[i] = -1

                if self.numbers[row * 5: row * 5 + 5] == [-1] * 5:
                    self.numbers[row * 5: row * 5 + 5] = [-2] * 5
                    self.iscomplete = True

                if self.numbers[col::5] == [-1] * 5:
                    self.numbers[col::5] = [-2] * 5
                    self.iscomplete = True
            except ValueError:
                pass

    def score(self, winningdraw):
        return winningdraw * sum([num for num in self.numbers if num >= 0]) 


def parse(filename):
    with open(filename) as stream:
        draws = list(map(int, stream.readline().split(',')))

        boardindex = 0
        boards = []
        while stream.readline():
            board = Board(boardindex=boardindex)
            board.fromstream(stream)
            boards.append(board)
            boardindex += 1

    return draws, boards


def play(draws, boards):
    completed = set()
    scores = []
    for draw in draws:
        for board in boards:
            board.draw(draw)
            if board.iscomplete:
                if board.boardindex not in completed:
                    completed.add(board.boardindex)
                    scores.append(board.score(draw))
                    if len(completed) == len(boards):
                        return scores


def tryexamples():
    draws, boards = parse('example.txt')
    scores = play(draws, boards)
    
    example1 = scores[0]
    print('example1', example1)
    assert example1 == 4512

    example2 = scores[-1]
    print('example2', example2)
    assert example2 == 1924


def main():
    tryexamples()
    draws, boards = parse('input.txt')
    scores = play(draws, boards)

    part1 = scores[0]
    print('part1', part1)

    part2 = scores[-1]
    print('part2', part2)


if __name__ == '__main__':
    main()