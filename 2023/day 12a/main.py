from puzzle import Puzzle


def parse(stream):
    puzzles = []
    for rawline in stream:
        line = rawline.strip()
        pattern, groupStr = line.split()
        groups = list(map(int, groupStr.split(',')))
        puzzles.append(Puzzle(pattern, groups))
    return puzzles


def part1(stream):
    total = 0
    for p in parse(stream):
        # should get the same totals by feeding groups in from the right and the left
        rightLen = p.arrangementLengthsRight(len(p), fullCheck=True)
        leftLen = p.arrangementLengthsLeft(len(p), fullCheck=True)
        assert sum(rightLen.values()) == sum(leftLen.values())
        # print(f'{p.pattern:20}\t{rightLen} = {sum(rightLen.values())}\t{leftLen} = {sum(leftLen.values())}')
        total += sum(rightLen.values())
    return total


def part2(stream):
    for p in parse(stream):
        # find the most compact leftwards arrangement for the 2x puzzle
        p2 = p.unfold(2)
        min2 = min(p2.arrangementLengthsLeft(len(p2)))
        print(min2, '/', len(p2))

        #! NB: arrangement lengths don't include the zero
        #!     that must appear between the LH and RH sides.
        #!     So as well as everything else, the sequences
        #!     cannot meet on a '#' (but this should be taken
        #!     into account by the extra mask bit check)


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 21, result

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    print(f'example2: {result}')
    #    assert result == 'xxxxx', result


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