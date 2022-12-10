class Board:
    def __init__(self, numbers):
        self.numbers = numbers
        self.mark = 25 * [False]
    
    def rc(index):
        row = index // 5
        col = index % 5
        return row, col

    def index(row, col):
        return row * 5 + col

    def __repr__(self):
        str = f'Board\n'
        for row in range(5):
            str += f'\t{self.numbers[row * 5: (row+1) * 5]}\n'
        return str


def parse(infile):
    draws = map(int, infile.readline().rstrip().split(','))
    boards = []
    while infile.readline():
        numbers = []
        for i in range(5):
            numbers += infile.readline().rstrip().split()
        assert len(numbers) == 25
        boards.append(Board(numbers))
    return draws, boards


def part1(draws, boards):
    pass


def part2():
    pass


def checkexamples():
    with open('example.txt') as infile:
        draws, boards = parse(infile)
        print(list(draws), boards)
    
    answer = (4512,)
    print('example 1', part1(draws, boards) == answer[0])



def main():
    checkexamples()
"""     with open('input.txt') as infile:
        print(part1())
        print(part2()) """

if __name__ == '__main__':
    main()