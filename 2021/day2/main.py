class Sub():
    def __init__(self, x=0, y=0, aim=0):
        self.x = x
        self.y = y
        self.aim = aim

    @property
    def depth(self):
        return -self.y

    @depth.setter
    def depth(self, value):
        self.y = -value

    def __repr__(self):
        return (f'Pos(x={self.x}, y={self.y}, aim={self.aim}) #depth {-self.depth}')

    def simplemove(self, cmd):
        dir, amount = cmd.split()
        amount = int(amount)
        if dir == 'forward':
            self.x += amount
        elif dir == 'down':
            self.y -= amount
        elif dir == 'up':
            self.y += amount
        elif dir == 'back':
            self.x -= amount
        else:
            raise ValueError
    
    def move(self, cmd):
        dir, amount = cmd.split()
        amount = int(amount)
        if dir == 'forward':
            self.x += amount
            self.depth += self.aim * amount
        elif dir == 'down':
            self.aim += amount
        elif dir == 'up':
            self.aim -= amount
        elif dir == 'back':
            self.x -= amount
            self.depth -= self.aim * amount
        else:
            raise ValueError
        

def part1(movelist):
    sub = Sub()
    for move in movelist:
        sub.simplemove(move)
    return sub.x * sub.depth

def part2(movelist):
    sub = Sub()
    for move in movelist:
        sub.move(move)
    return sub.x * sub.depth

def checkexamples():
    examples = [
        (('forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2'), (150, 900)),
    ]
    for data, answer in examples:
        assert part1(data) == answer[0]
        assert part2(data) == answer[1]


def main():
    checkexamples()
    with open('input.txt') as infile:
        movelist = infile.readlines()
        print(part1(movelist))
        print(part2(movelist))

if __name__ == '__main__':
    main()