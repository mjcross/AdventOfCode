from parse import parse
from puzzle import Puzzle

nbits = [2**n - 1 for n in range(25)]

def num_combos(p:Puzzle, depth:int):
    print(depth * '\t', 'counting combinations for', p)

    n = 0
    sz = p.groups.popleft()
    for pos in range(0, p.length - sz + 1):
        x = nbits[sz] << pos

        # check whether pos is allowed
        mask = nbits[pos + sz + 1]  # add one for the gap between groups
        print(depth * '\t', f'checking {x:020b} with mask {mask:020b} ', end='')
        if (p.clrbits & mask & x):
            print('clr!')
            continue    # not allowed: clrbits are set
        if (p.setbits & mask & x) != (p.setbits & mask):
            print('set!')
            continue    # not allowed: setbits are clear

        print('OK')

        if p.groups:
            # place remaining groups
            n += num_combos(
                Puzzle(
                    groups=p.groups.copy(),
                    length=p.length - (pos + sz + 1),
                    setbits=p.setbits >> (pos + sz + 1),
                    clrbits=p.clrbits >> (pos + sz + 1)
                ), 
                depth + 1
            )
            print(depth * '\t', 'count is now', n)
        else:
            # all groups are placed - valid combo
            n += 1
            print(depth * '\t', 'valid combo (', n, ')')

    print(depth * '\t', 'tried all valid positions for sz=', sz, ': count=', n)
    return n



def part1(stream):
    puzzles, lines = parse(stream)
    total = 0
    for puzzle, line in zip(puzzles, lines):
        num_valid = num_combos(puzzle, 0)
        print(line)
        print(num_valid)
        print()
        total += num_valid
    return total


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
    #    assert result == 'xxxxx', result

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    print(f'example2: {result}')
    #    assert result == 'xxxxx', result


def main():
    #checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    #with open('input.txt') as stream:
    #    result = part2(stream)
    #    print(f'part2 {result}')


if __name__ == '__main__':
    main()