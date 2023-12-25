from grid import IntGrid
from enum import Enum
from dataclasses import dataclass
from copy import deepcopy

class Dir(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)

    @property
    def recip(self):
        if self is Dir.N:
            return Dir.S
        elif self is Dir.E:
            return Dir.W
        elif self is Dir.S:
            return Dir.N
        elif self is Dir.W:
            return Dir.E
        else:
            raise ValueError


@dataclass
class Head:
    x: int
    y: int
    straightCount: int
    dir: Dir
    cost: int
    wayOut: tuple
    grid: IntGrid

    @property
    def score(self):
        # average cost per step is 5
        d = (self.wayOut[0] - self.x) + self.y
        return self.cost + 5 * d
    
    def __eq__(self, other):
        return self.score == other.score
    
    def __gt__(self, other):
        return self.score > other.score
    
    def __lt__(self, other):
        return self.score < other.score
    
    def nextHeads(self):
        """Returns a list of all possible tiles reachable in the next step."""
        nextHeads = []

        # if we are at the exit then there are no further steps
        if (self.x, self.y) == self.wayOut:
            return [self]

        # all possible directions from this head
        for dir in Dir:
            if dir is self.dir.recip:
                # can't turn 180 degrees
                continue
            if dir == self.dir:
                if self.straightCount >= 3:
                    # can't go more than three steps in the same direction
                    continue
                else:
                    straightCount = self.straightCount + 1
            else:
                # we turned left or right
                straightCount = 1

            dx, dy = dir.value
            x = self.x + dx
            y = self.y + dy
            
            try:
                cost = self.cost + self.grid[x, y]
            except IndexError:
                # went off the edge of the grid
                continue

            nextHeads.append(Head(
                x=x,
                y=y,
                straightCount=straightCount,
                dir=dir,
                cost=cost,
                wayOut=self.wayOut,
                grid=self.grid
            ))

        return nextHeads


def readIntGrid(stream):
    # find dimensions of grid
    width = len(stream.readline().strip('\n'))

    height = 1
    while stream.readline():
        height += 1

    # rewind stream and initialise grid
    stream.seek(0)
    return IntGrid(width, height, list([line.strip('\n') for line in stream]))


def part1(stream):
    grid = readIntGrid(stream)
    wayOut = (grid.width - 1, 0)
    numLookAhead = 13   # number of moves to look ahead for each position

    best = IntGrid(grid.width, grid.height)
    
    head = Head(
        x=0, y=grid.height - 1,
        straightCount=0,
        dir=Dir.E,
        cost=0,
        wayOut=wayOut,
        grid=grid)
    
    while (head.x, head.y) != wayOut:
        # find the next steps from this head
        #todo: we may need to follow several heads until we reach maxHeads
        nextHeads = head.nextHeads()

        # score the next steps by looking ahead
        scores = []
        for h in nextHeads:

            # identify the places we can reach from this next step
            lookAheads = [h]
            for stepNum in range(numLookAhead):
                nextLookAheads = []
                for h in lookAheads:
                    nextLookAheads += h.nextHeads()
                lookAheads = nextLookAheads
            
            # find the lowest cost place
            bestScore = min(lookAheads).score

            scores.append(bestScore)
        
        # go the most promising way
        bestScore = min(scores)
        head = nextHeads[scores.index(bestScore)]

        best[head.x, head.y] = head.cost
        print(best)
        pass

    return head.cost




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
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    #with open('input.txt') as stream:
    #    result = part2(stream)
    #    print(f'part2 {result}')


if __name__ == '__main__':
    main()