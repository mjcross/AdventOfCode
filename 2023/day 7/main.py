from parse import parse, parse2


def part1(stream):
    hands = parse(stream)
    hands.sort()
    winnings = 0
    for index, hand in enumerate(hands):
        winnings += (index+1) * hand.bid
    return winnings


def part2(stream):
    hands = parse2(stream)
    hands.sort()
    winnings = 0
    for index, hand in enumerate(hands):
        winnings += (index+1) * hand.bid
    return winnings


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 6440, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 5905, result

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