from grid import IntGrid
from enum import IntEnum
from dataclasses import dataclass

class Dir(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

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
        
    @property
    def move(self):
        if self is Dir.N:
            return (0, 1)
        elif self is Dir.E:
            return (1, 0)
        elif self is Dir.S:
            return (0, -1)
        elif self is Dir.W:
            return (-1, 0)
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
    path: list[(int, int)]

    @property
    def score(self):
        # average cost per step is 5
        # d = (self.wayOut[0] - self.x) + self.y
        return self.cost
        #return self.cost + 5 * d
    
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

            dx, dy = dir.move
            x = self.x + dx
            y = self.y + dy
            
            try:
                cost = self.cost + self.grid[x, y]
            except IndexError:
                # went off the edge of the grid
                continue

            nextPath = self.path.copy()
            nextPath.append((x, y))
            nextHeads.append(Head(
                x=x,
                y=y,
                straightCount=straightCount,
                dir=dir,
                cost=cost,
                wayOut=self.wayOut,
                grid=self.grid,
                path=nextPath
            ))

        return nextHeads

    def nextHeadsUltra(self):
        nextHeads = []

        # if we are at the exit then this must be our 4th step in the same
        # direction or we can't stop!
        if (self.x, self.y) == self.wayOut:
            if self.straightCount == 3:
                return [self]
            else:
                return []

        # all possible directions from this head
        for dir in Dir:
            if dir is self.dir.recip:
                # can't turn 180 degrees
                continue

            if dir == self.dir:
                if self.straightCount >= 10:
                    # can't move more than ten steps in the same direction
                    continue
                else:
                    straightCount = self.straightCount + 1
            else:
                # we are attempting to turn...
                # but this is not permitted until having gone at least 
                # four steps in the same direction
                if self.straightCount <= 3:
                    continue
                else:
                    straightCount = 1

            dx, dy = dir.move
            x = self.x + dx
            y = self.y + dy
            
            try:
                cost = self.cost + self.grid[x, y]
            except IndexError:
                # went off the edge of the grid
                continue

            nextPath = self.path.copy()
            nextPath.append((x, y))
            nextHeads.append(Head(
                x=x,
                y=y,
                straightCount=straightCount,
                dir=dir,
                cost=cost,
                wayOut=self.wayOut,
                grid=self.grid,
                path=nextPath
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
    maxHeads = 150_000

    cost = IntGrid(grid.width, grid.height)

    # separate score tables for each straightCount and direction
    scores = [0,
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)], 
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)]]
    
    heads = [Head(
        x=0, y=grid.height - 1,
        straightCount=0,
        dir=Dir.E,
        cost=0,
        wayOut=wayOut,
        grid=grid,
        path=[(0, grid.height - 1)])]
    
    finalCosts = []
    while heads:
        nextHeads = {}

        for head in heads:
            if (head.x, head.y) == wayOut:
                finalCosts.add(head)
            
            else:            
                neighbours = head.nextHeads()
                for h in neighbours:
                    if (h.x, h.y) == wayOut:
                        finalCosts.append(h)
                    elif scores[h.straightCount][h.dir][h.x, h.y] == 0 or h.score < scores[h.straightCount][h.dir][h.x, h.y]:
                            # replace inferior-scoring head with the same straightCount
                            nextHeads[h.x, h.y, h.dir, h.straightCount] = h
                            scores[h.straightCount][h.dir][h.x, h.y] = h.score
                            cost[h.x, h.y] = h.cost

        #print(cost)
        print(len(nextHeads))
        heads = nextHeads.values()

    bestCost = min(finalCosts)
    path = bestCost.path
    best = IntGrid(grid.width, grid.height)
    cost = 0
    for x, y in path[1:]:
        cost += grid[x, y]
        best[x, y] = cost

    print(best)

    return bestCost.cost



def part2(stream):
    grid = readIntGrid(stream)
    wayOut = (grid.width - 1, 0)
    maxHeads = 150_000

    cost = IntGrid(grid.width, grid.height)

    # separate score tables for each straightCount and direction
    scores = [0,
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)], 
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)],
              [IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height), IntGrid(grid.width, grid.height)]]
    
    heads = [Head(
        x=0, y=grid.height - 1,
        straightCount=0,
        dir=Dir.E,
        cost=0,
        wayOut=wayOut,
        grid=grid,
        path=[(0, grid.height - 1)])]
    
    finalCosts = []
    while heads:
        nextHeads = {}

        for head in heads:
            if (head.x, head.y) == wayOut:
                finalCosts.add(head)
            
            else:            
                neighbours = head.nextHeadsUltra()
                for h in neighbours:
                    if (h.x, h.y) == wayOut:
                        finalCosts.append(h)
                    elif scores[h.straightCount][h.dir][h.x, h.y] == 0 or h.score < scores[h.straightCount][h.dir][h.x, h.y]:
                            # replace inferior-scoring head with the same straightCount
                            nextHeads[h.x, h.y, h.dir, h.straightCount] = h
                            scores[h.straightCount][h.dir][h.x, h.y] = h.score
                            cost[h.x, h.y] = h.cost

        #print(cost)
        print(len(nextHeads))
        heads = nextHeads.values()

    bestCost = min(finalCosts)
    path = bestCost.path
    best = IntGrid(grid.width, grid.height)
    cost = 0
    for x, y in path[1:]:
        cost += grid[x, y]
        best[x, y] = cost

    print(best)

    return bestCost.cost


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 102, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 94, result


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