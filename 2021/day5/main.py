from collections import namedtuple, Counter
Point = namedtuple('Point', 'x y')

class Segment:
    def __init__(self, rowstr):
        pointstrs = rowstr.strip().split(' -> ')
        self.pointa, self.pointb = [Point(*map(int, str.split(','))) for str in pointstrs]

    def __repr__(self):
        return f'Segment(\n\t{self.pointa}\n\t{self.pointb}\n)'

    def isvert(self):
        return self.pointa.x == self.pointb.x
        
    def ishoriz(self):
        return self.pointa.y == self.pointb.y

    def points(self):
        xa, ya = self.pointa.x, self.pointa.y
        xb, yb = self.pointb.x, self.pointb.y
        dx = max(min(xb - xa, 1), -1)
        dy = max(min(yb - ya, 1), -1)
        x, y = xa, ya
        while x != xb or y != yb:
            yield Point(x, y)
            x += dx
            y += dy
        yield Point(x, y)


def part1(stream):
    counter = Counter()
    for line in stream:
        segment = Segment(line)
        if segment.ishoriz() or segment.isvert():
            counter.update(segment.points())

    numoverlaps = 0
    for count in counter.values():
        if count >= 2:
            numoverlaps += 1
    return numoverlaps


def part2(stream):
    counter = Counter()
    for line in stream:
        segment = Segment(line)
        counter.update(segment.points())

    numoverlaps = 0
    for count in counter.values():
        if count >= 2:
            numoverlaps += 1
    return numoverlaps


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream)
        assert example1 == 5, example1

    with open('example.txt') as stream:
        example2 = part2(stream)
        assert example2 == 12, example1


def main():
    checkexamples()
    with open('input.txt') as stream:
        print('part1', part1(stream))

    with open('input.txt') as stream:
        print('part2', part2(stream))

if __name__ == '__main__':
    main()