from dataclasses import dataclass


def binStr(x: int, nBits: int) -> str:
    """ Returns the string representation of a binary number padded with leading zeroes. """
    return f'{x:0{nBits}b}'

nBits = [2**n - 1 for n in range(200)]


@dataclass
class Puzzle:
    pattern: str
    groups: list[int]

    def __len__(self):
        return len(self.pattern)

    def __post_init__(self):
        setBits = 0
        clrBits = 0
        for c in self.pattern:
            setBits <<= 1
            clrBits <<= 1
            if c == '#':
                setBits |= 1
            elif c == '.':
                clrBits |= 1
        self.setBits = setBits
        self.clrBits = clrBits

    def __str__(self):
        s = f'     {self.pattern} ({len(self)}) {self.groups}'
        s += f'\nset: {binStr(self.setBits, len(self))} '
        s += f'\nclr: {binStr(self.clrBits, len(self))} '
        return s

    def _placeGroup(self, x, groupNum, start) -> int:
        nValid = 0
        sz = self.groups[groupNum]
        minLeft = sum(self.groups[:groupNum]) + groupNum + 1
        bits = nBits[sz]
        maxShift = len(self) - minLeft - sz + 1
        for shift in range(start, maxShift + 1):
            tryX = x | bits << shift
            if groupNum == 0:
                # last group - full check
                mask = nBits[len(self)]
            else:
                # not the last group - check only covered groups
                mask = nBits[shift + sz + 1]

            if (tryX & self.clrBits) == 0 and ((tryX ^ mask) & self.setBits) == 0:
                # valid placement of group
                if groupNum == 0:
                    # valid arrangement
                    nValid += 1
                else:
                    # place next group
                    nValid += self._placeGroup(x=tryX, groupNum=groupNum - 1, start=shift + sz + 1)
        return nValid
    
    def nArrangements(self) -> int:
        return self._placeGroup(0, len(self.groups) - 1, 0)

    def unfold(self, mult):
        return Puzzle('?'.join(mult * [self.pattern]), mult * self.groups)
    

def main():
    # check we get the same number of leftwards and rightwards arrangements
    p = Puzzle('?#?#?#????????.', [8, 1])
    print(p.pattern)

    rightLen = p.arrangementLengthsRight(len(p), fullCheck=True)
    print(f'{rightLen} = {sum(rightLen.values())}')

    leftLen = p.arrangementLengthsLeft(len(p), fullCheck=True)
    print(f'{leftLen} = {sum(leftLen.values())}')

    assert sum(rightLen.values()) == sum(leftLen.values())

    print(p.nArrangements())

if __name__ == '__main__':
    main()