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

    def _placeGroupR(self, x, length, lengthDir, groupNum, start=0, fullCheck=False):
        #print(f'placing group[{groupNum}]:', self.groups[groupNum])
        sz = self.groups[groupNum]
        minLeft = sum(self.groups[:groupNum]) + groupNum + 1    # minimum space taken up by remaing groups and padding
        #print(minLeft)
        bits = nBits[sz]
        maxShift = length - minLeft - sz + 1    # leave space for remaining groups and padding
        #print('    ', binStr(bits << maxShift, len(self)), 'max shift')
        for shift in range(start, maxShift + 1):
            tryX = x | bits << shift
            mask = nBits[shift + sz + 1]
            #print('    ', binStr(mask, len(self)), 'mask')
            #print('    ', binStr(tryX,len(self)), end=' ')
            if (tryX & self.clrBits) == 0 and ((tryX ^ mask) & self.setBits) == 0:
                if groupNum == 0:
                    # all groups placed
                    if fullCheck and ((tryX ^ nBits[length]) & self.setBits) != 0:
                        # higher order setBits aren't set
                        #print('failed full check')
                        #print(binStr(tryX, len(self)))
                        pass
                    else:
                        # record valid arrangment
                        #print(f'valid arrangement ({shift + sz})')
                        lengthDir[shift + sz] = lengthDir.get(shift + sz, 0) + 1
                        #print('    ', binStr(tryX, len(self)))
                else:
                    # place next group
                    self._placeGroupR(tryX, length, lengthDir, groupNum - 1, shift + sz + 1, fullCheck)
            #else:
            #    print('invalid')

    def _placeGroupL(self, x, length, lengthDir, groupNum, end=None, fullCheck=False):
        if end is None:
            end = length
        #print(f'placing group[{groupNum}]:', self.groups[groupNum])
        sz = self.groups[groupNum]
        minRight = sum(self.groups[groupNum + 1:]) + len(self.groups) - groupNum
        #print(minRight)
        bits = nBits[sz]
        minShift = minRight - 1
        #print('    ', binStr(bits << minShift, len(self)), 'min shift')
        for shift in range(end - sz, minShift - 1, -1):
            tryX = x | bits << shift
            
            if shift > 0:
                mask = nBits[length - (shift - 1)] << (shift - 1)
            else:
                mask = nBits[length]

            #print('    ', binStr(mask, len(self)), 'mask')
            #print('    ', binStr(tryX,len(self)), end=' ')
            if (tryX & self.clrBits) == 0 and ((tryX ^ mask) & self.setBits) == 0:
                #print('valid')
                if groupNum == len(self.groups) - 1:
                    # all groups placed
                    if fullCheck and ((tryX ^ (nBits[length] << (len(self) - length))) & self.setBits) != 0:
                        # higher order setBits aren't set
                        #print('failed full check')
                        #print(binStr(tryX, len(self)))
                        pass
                    else:
                        # record valid arrangment
                        #print(f'valid arrangement ({len(self) - shift})')
                        lengthDir[len(self) - shift] = lengthDir.get(len(self) - shift, 0) + 1
                        #print('    ', binStr(tryX, len(self)))
                else:
                    # place next group
                    self._placeGroupL(tryX, length, lengthDir, groupNum + 1, shift - 1, fullCheck)
            #else:
            #    print('invalid')


    def arrangementLengthsRight(self, length, fullCheck=False) -> dir:
        """ Returns counts of valid arrangement lengths when groups are fed in from the right. """
        lengthDir = {}
        self._placeGroupR(
            x=0, 
            length=length, 
            lengthDir=lengthDir, 
            groupNum=len(self.groups)-1, 
            start=0, 
            fullCheck=fullCheck)
        return lengthDir
    
    def arrangementLengthsLeft(self, length, fullCheck=False) -> dir:
        """ Returns counts of valid arrangement lengths when groups are fed in from the left. """
        lengthDir = {}
        self._placeGroupL(
            x=0, 
            length=length, 
            lengthDir=lengthDir, 
            groupNum=0, 
            end=len(self), 
            fullCheck=fullCheck)
        return lengthDir

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

    # check we can solve half the double puzzle with the same result 
    p2 = Puzzle('?#?#?#????????.??#?#?#????????.', [8, 1])
    print(p2.pattern)

    r2 = p2.arrangementLengthsRight(len(p), fullCheck=True)
    print(f'{r2} = {sum(r2.values())}')
    assert r2 == rightLen

    l2 = p2.arrangementLengthsLeft(len(p), fullCheck=True)
    print (f'{l2} = {sum(l2.values())}')
    assert l2 == leftLen

if __name__ == '__main__':
    main()