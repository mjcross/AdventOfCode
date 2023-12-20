from parse import Puzzle, parse

def nDiffs(s1, s2):
    return sum(1 for c1, c2 in zip(s1, s2) if c1 != c2)


def findSymmetry(rows, nErrs=0) -> list[int]:
    # find first symmetry with a given number of errors
    nRows = len(rows)
    for symRow in range(1, nRows):
        rowsAbove = rows[:symRow]
        rowsBelow = rows[symRow:]

        nAbove = len(rowsAbove)
        nBelow = len(rowsBelow)

        if nAbove > nBelow:
            rowsAbove = rowsAbove[-nBelow:]
        elif nBelow > nAbove:
            rowsBelow = rowsBelow[:nAbove]

        rowsBelow.reverse()

        errCount = 0
        for row1, row2 in zip(rowsAbove, rowsBelow):
            errCount += nDiffs(row1, row2)
        
        if errCount == nErrs:
            return symRow
    return 0


def part1(stream):
    total = 0
    for puzzle in parse(stream):
        # vertical reflections
        vSyms = findSymmetry(puzzle.cols)

        # horizontal reflections
        hSyms = findSymmetry(puzzle.rows)

        total += vSyms + 100 * hSyms
    return total


def part2(stream):
    total = 0
    for puzzle in parse(stream):
        # find symmetries with one error
        vSyms = findSymmetry(puzzle.cols, 1)

        # horizontal reflections
        hSyms = findSymmetry(puzzle.rows, 1)

        total += vSyms + 100 * hSyms
    return total


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 405, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
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