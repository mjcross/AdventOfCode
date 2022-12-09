class Pos:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def astuple(self):
        return (self.x, self.y)
    
    def __repr__(self):
        return f'Pos({self.x}, {self.y})'


def parseinput(filename):
    moves = ''
    with open(filename) as file:
        for line in file:
            dir, num = line.split()
            moves += dir * int(num)
    return moves


def part1(moves, numknots):
    knots = []
    for _ in range(numknots):
        knots.append(Pos())
    tailvisited = set({knots[-1].astuple})

    for move in moves:
        if move == 'U':
            knots[0].y += 1
        elif move == 'D':
            knots[0].y -= 1
        elif move == 'R':
            knots[0].x += 1
        elif move == 'L':
            knots[0].x -= 1
        else:
            raise ValueError(f'move: {move}')

        prevknot = knots[0]
        for knot in knots[1:]:
            xerr = knot.x - prevknot.x
            yerr = knot.y - prevknot.y

            if abs(xerr) > 1 or abs(yerr) > 1:
                touching = False
            else:
                touching = True

            if not touching:
                if xerr < 0:
                    knot.x += 1
                if xerr > 0:
                    knot.x -= 1
                if yerr < 0:
                    knot.y += 1
                if yerr > 0:
                    knot.y -= 1

            prevknot = knot

       #print(f'after {move} {knots}')

        tailvisited.add(knots[-1].astuple)
    return len(tailvisited)


def checkexamples():
    moves = parseinput('example.txt')    

    example1 = part1(moves, 2)
    print('example part1', example1)
    assert example1 == 13

    moves = parseinput('example2.txt')
    example2 = part1(moves, 10)
    print('example part2', example2)
    assert example2 == 36


def main():
    checkexamples()
    moves = parseinput('input.txt')
    print(part1(moves, 2))
    print(part1(moves, 10))


if __name__ == '__main__':
    main()