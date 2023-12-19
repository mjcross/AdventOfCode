from puzzle import Puzzle

def binstr(bits:int, nbits:int):
    return f'{bits:0{nbits}b}'


def puzzleFromStr(patternStr: str, groups: list[int]) -> Puzzle:
    length = len(patternStr)
    setbits = 0
    clrbits = 0
    for c in patternStr:
        setbits <<= 1
        clrbits <<= 1
        if c == '#':
            setbits |= 1
        elif c == '.':
            clrbits |= 1

    #print(patternStr, 'set:', binstr(setbits, length), 'clr:', binstr(clrbits, length))
    return Puzzle(length, setbits, clrbits, groups.copy(), patternStr)


def parse(stream) -> list[Puzzle]:
    puzzles = []
    for rawline in stream:
        line = rawline.strip()

        patternStr, groupsStr = line.split()

        groups = list(map(int, groupsStr.split(',')))

        while '..' in patternStr:
            patternStr = patternStr.replace('..', '.')

        puzzles.append(puzzleFromStr(patternStr, groups))

    return puzzles