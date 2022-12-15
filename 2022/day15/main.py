from utils.range import Range
import timeit


def mdist(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)


class Sensor:
    def __init__(self, xs, ys, xb, yb):
        self.range = mdist(xs, ys, xb, yb)
        self.x, self.y = xs, ys
        self.xb, self.yb = xb, yb

    def __repr__(self):
        return f'Sensor at ({self.x}, {self.y}) closest beacon ({self.xb}, {self.yb}) range {self.range}'

    def rowrange(self, row):
        dy = abs(row - self.y)
        if dy > self.range:
            return None
        else:
            dx = self.range - dy
            return Range(min=self.x - dx, max=self.x + dx)


def parse(stream):
    sensors = []
    beacons = set()
    for line in stream:
        field = [string.strip('\n,:') for string in line.split()]
        xs = int(field[2].split('=')[1])
        ys = int(field[3].split('=')[1])
        xb = int(field[8].split('=')[1])
        yb = int(field[9].split('=')[1])
        sensors.append(Sensor(xs, ys, xb, yb))
        beacons.add((xb, yb))
    return sensors, beacons


def part1(stream, rownum):
    sensors, beacons = parse(stream)
    rowranges = []
    for sensor in sensors:
        rowrange = sensor.rowrange(rownum)
        if rowrange:
            rowranges = rowrange.addtolist(rowranges)
    squarescovered = sum([len(rowrange) for rowrange in rowranges])
    numbeacons = len([True for beacon in beacons if beacon[1] == rownum])
    return squarescovered - numbeacons


def part2(stream, maxordinate):
    sensors, beacons = parse(stream)
    for rownum in range(maxordinate + 1):
        if rownum and rownum % 10000 == 0:
            print('.', end='', flush=True)
        rowranges = []
        for sensor in sensors:
            rowrange = sensor.rowrange(rownum)
            if rowrange:
                rowranges = rowrange.addtolist(rowranges)
        if len(rowranges) > 1:
            r1, r2 = rowranges[0: 2]
            x1 = r2.min - r1.max
            x2 = r1.min - r2.max
            
            assert (x1 == 2 or x2 == 2)
            if x1 == 2:
                x = r1.max + 1
            else:
                x = r2.max + 1
            y = rownum
            return x * 4000000 + y


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream, rownum=10)
        assert example1 == 26, example1

    with open('example.txt') as stream:
        example2 = part2(stream, 20)
        assert example2 == 56000011, example2


def main():
    checkexamples()

    with open('input.txt') as stream:
        print('part1', part1(stream, 2000000))

    with open('input.txt') as stream:
        print ('part2', end=' ')
        start = timeit.default_timer()
        print(part2(stream, 4000000))
        stop = timeit.default_timer()
        print(f'elasped: {stop - start:.2f}')

if __name__ == '__main__':
    main()