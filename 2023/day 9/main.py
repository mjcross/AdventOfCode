from parse import parse
from extrapolate import extrapolate


def part1(stream):
    sequences = parse(stream)
    sum = 0
    for seq in sequences:
        sum += extrapolate(seq)[0]
    return sum


def part2(stream):
    sequences = parse(stream)
    sum = 0
    for seq in sequences:
        sum += extrapolate(seq)[-1]
    return sum


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 114, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 2, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()