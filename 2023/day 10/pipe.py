from enum import IntEnum
from dataclasses import dataclass, field

class Dir(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    @property
    def inverse(self):
        return [Dir.S, Dir.W, Dir.N, Dir.E][self.value]

    @property
    def dxdy(self):
        return [(0, 1), (1, 0), (0, -1), (-1, 0)][self.value]
    
    def __str__(self):
        return self.name

@dataclass
class Pipe:
    symbol: str
    ports: list[Dir] = field(default_factory=list)
    
    def hasPort(self, dir):
        return dir in self.ports

    def isAccessibleHeading(self, dir):
        if self.symbol == 'S':
            # 'S' is accessible from any direction
            return True
        else:
            return dir.inverse in self.ports

    def nextDir(self, dir):
        if self.ports[0] is dir.inverse:
            return self.ports[1]
        elif self.ports[1] is dir.inverse:
            return self.ports[0]
        raise ValueError

pipes = {
    '|': Pipe('|', [Dir.N, Dir.S]),
    '-': Pipe('-', [Dir.E, Dir.W]),
    'L': Pipe('L', [Dir.N, Dir.E]),
    'J': Pipe('J', [Dir.N, Dir.W]),
    '7': Pipe('7', [Dir.S, Dir.W]),
    'F': Pipe('F', [Dir.S, Dir.E]),
    '.': Pipe('.', []),
    'S': Pipe('S', [])
}

def main():
    # simple test cases
    Dir.N.inverse is Dir.S
    assert pipes['J'].hasPort(Dir.W)
    assert pipes['J'].isAccessibleHeading(Dir.E)
    assert pipes['J'].nextDir(Dir.E) is Dir.N
    print('tests OK')

if __name__ == '__main__':
    main()