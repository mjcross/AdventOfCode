from parse import parse, puzzleFromStr
from puzzle import iterate, unfold, groupLengths, shortestGroup, reversedPuzzle

def part1(stream):
    puzzles = parse(stream)
    total = 0
    for puzzle in puzzles:
        total += iterate(puzzle, 0, 0)
    return total


def part2(stream):
    puzzles: list[puzzle] = parse(stream)
    for puzzle in puzzles:

        #print(puzzle.text, puzzle.length)

        # find most compact right-justified arrangement for 3x unfolding
        min_3 = shortestGroup(unfold(puzzle, 3))
        #print(min_3)

        # find most compact left-justified arrangement for 2x unfolding
        revPuzzle = reversedPuzzle(puzzle)
        min_2 = shortestGroup(unfold(revPuzzle, 2))
        #print(min_2)

        # get the 5x unfolding
        p5 = unfold(puzzle, 5)
        
        #? these may need to be a couple of chars longer
        puzz_3 = p5.text[min_2 - 1:]
        puzz_2 = p5.text[:p5.length - min_3]
        
        # parts of the p5 puzzle not covered by the most compact arrangements
        p3 = puzzleFromStr(puzz_3, 3 * puzzle.groups.copy())
        p2 = reversedPuzzle(puzzleFromStr(puzz_2, 2 * puzzle.groups.copy()))
        print(p3)
        print(p2)

        g3 = groupLengths(p3)
        g2 = groupLengths(p2)

        # sum products of frequencies of groups that don't exceed the p5 length
        n5 = 0
        for l3, n3 in g3.items():
            for l2, n2 in g2.items():
                if l2 + l3 <= (p5.length + 1):
                    print(l2, l3, l2 + l3)
                    n5 += n2 * n3

        print(n5, iterate(p5, 0, 0))
 


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 21, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 525152, result


def main():
    #checkexamples()

    #with open('input.txt') as stream:
    #    result = part1(stream)
    #    print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()