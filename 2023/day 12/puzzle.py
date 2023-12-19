from dataclasses import dataclass

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

    def _placeGroup(self, x, groupNum, start, cache) -> int:
        """
        Finds all the valid placings of group[groupNum], starting at pattern
        index 'start', and then recursively places the remaining groups and 
        returns the total number of valid arrangements that can be reached
        from this starting point.
        """

        #! check cache
        if (groupNum, start) in cache:
            return cache[(groupNum, start)]

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
                    nFollowing = self._placeGroup(
                        x=tryX, 
                        groupNum=groupNum - 1, 
                        start=shift + sz + 1, 
                        cache=cache)
                    nValid += nFollowing

        #! save result in cache
        cache[(groupNum, start)] = nValid

        return nValid
    
    def nArrangements(self) -> int:
        return self._placeGroup(0, len(self.groups) - 1, 0, {})

    def unfold(self, mult):
        return Puzzle('?'.join(mult * [self.pattern]), mult * self.groups)   