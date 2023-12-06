from card import Card
from parse import parse

def part1(stream):
    totScore = 0
    for card in parse(stream):
        totScore += card.getScore
    return totScore


def part2(stream):
    # build a directory of the pre-computed copies won by each card
    cardCopies = {card.num:card.copies for card in parse(stream)}
    stream.seek(0)

    # start with the original set of cards
    newCards = [card.num for card in parse(stream)]
    cardCount = 0

    # iterate until we don't get any new copies
    while newCards:
        cardCount += len(newCards)
        cards = newCards.copy()
        newCards = []
        for card in cards:
            newCards += cardCopies[card]
    return cardCount


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 13, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 30, result


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