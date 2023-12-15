from dataclasses import dataclass
from collections import deque

nbits = [2**n - 1 for n in range(25)]

@dataclass
class Puzzle:
    length: int
    setbits: int
    clrbits: int
    groups: deque[int]

    def __str__(self):
        return f'length={self.length}, setbits={bin(self.setbits)}, clrbits={bin(self.clrbits)}, groups={self.groups}'

    def solve(self):
        end = self.length
        x = 0
        self.ends = deque()
        # start by fitting each group as far as possible to the right
        rGroups = []
        for sz in reversed(self.groups):
            self.ends.appendleft(end)
            pos = end - sz
            bits = nbits[sz] << pos
            while True:
                if (bits & self.clrbits) == 0:
                    break
                bits >>= 1
                pos -= 1
                if pos < 0:
                    raise IndexError
            x |= bits
            end = pos - 1  # leave a gap
    
        # self.ends[] now has the effective 'length' for each group
