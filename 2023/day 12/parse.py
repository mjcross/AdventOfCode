from collections import deque
from puzzle import Puzzle

def parse(stream):
    puzzles = []
    lines = []
    for rawline in stream:
        line = rawline.strip()
        lines.append(line)
        maskstr, groupsstr = line.split()

        # remove leading, trailing and repeated '.'
        maskstr = maskstr.strip('.')
        while '..' in maskstr:
            maskstr = maskstr.replace('..', '.')

        # work out which bits must be set and clear
        length = len(maskstr)
        setbits = 0
        clrbits = 0
        maskbit = 1
        for c in maskstr:
            if c == '.':
                clrbits |= maskbit
            elif c == '#':
                setbits |= maskbit
            maskbit <<= 1

        # parse group lengths
        groups = deque(map(int, groupsstr.split(',')))

        # make Puzzle instance
        puzzles.append(Puzzle(length, setbits, clrbits, groups))

    return puzzles, lines