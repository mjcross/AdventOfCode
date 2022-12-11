from collections import deque


class Monkey:
    def __init__(self, stream):
        self.fromstream(stream)
        self.inspected = 0

    def __repr__(self):
        return (
            f'Monkey {self.number}:\n'
            f'\titems {self.items}\n'
            f'\tiftrue {self.iftrue}\n'
            f'\tiffalse {self.iffalse}\n'
            f'\tinspected {self.inspected}\n'
        )

    def fromstream(self, stream):
        field = stream.readline().split()
        assert field[0] == 'Monkey', field
        self.number = int(field[1].strip(':'))

        field = stream.readline().split()
        assert field[0] == 'Starting', field
        self.items = deque([int(item.strip(',')) for item in field[2:]])

        field = stream.readline().split()
        assert field[0] == 'Operation:', field
        opcode = field[4]
        operand = field[5]
        if opcode == '*':
            if operand == 'old':
                self.operation = lambda old: old * old
            else:
                self.operation = lambda old: old * int(operand)
        elif opcode == '+':
            if operand == 'old':
                self.operation = lambda old: old + old
            else:
                self.operation = lambda old: old + int(operand)
        else:
            raise ValueError('opcode', opcode)

        field = stream.readline().split()
        assert field[0:3] == ['Test:', 'divisible', 'by'], field
        radix = int(field[3])
        self.test = lambda x: x % radix == 0
        self.radix = radix

        field = stream.readline().split()
        assert field[0:5] == ['If', 'true:', 'throw', 'to', 'monkey'], field
        self.iftrue = int(field[5])

        field = stream.readline().split()
        assert field[0:5] == ['If', 'false:', 'throw', 'to', 'monkey'], field
        self.iffalse = int(field[5])


def parse(stream):
    monkeys = []
    while True:
        monkeys.append(Monkey(stream))
        if not stream.readline():
            return monkeys


def monkeybusiness(stream, worrydivisor=3, numrounds=20):
    monkeys = parse(stream)
    for roundnum in range(numrounds):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.items.popleft()
                monkey.inspected += 1
                item = monkey.operation(item)
                item = item // worrydivisor
                if monkey.test(item):
                    monkeys[monkey.iftrue].items.append(item)
                else:
                    monkeys[monkey.iffalse].items.append(item)
    mostactive = sorted(monkeys, key=lambda monkey: monkey.inspected, reverse=True)
    monkeybusiness = mostactive[0].inspected * mostactive[1].inspected
    return monkeybusiness


def monkeybusiness2(stream, numrounds=10000):
    monkeys = parse(stream)
    lcm = 1
    for monkey in monkeys:
        lcm *= monkey.radix
    for roundnum in range(numrounds):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.items.popleft()
                monkey.inspected += 1
                item = monkey.operation(item)
                item = item % lcm
                if monkey.test(item):
                    monkeys[monkey.iftrue].items.append(item)
                else:
                    monkeys[monkey.iffalse].items.append(item)
    mostactive = sorted(monkeys, key=lambda monkey: monkey.inspected, reverse=True)
    monkeybusiness = mostactive[0].inspected * mostactive[1].inspected
    return monkeybusiness


def checkexamples():
    with open('example.txt') as stream:
        example1 = monkeybusiness(stream)
        print('example1', example1)
        assert example1 == 10605, example1

    with open('example.txt') as stream:
        example2 = monkeybusiness2(stream, numrounds=10000)
        print('example2', example2)
        assert example2 == 2713310158, example2


def main():
    checkexamples()

    with open('input.txt') as stream:
        part1 = monkeybusiness(stream)
        print('part1', part1)
    
    with open('input.txt') as stream:
        part2 = monkeybusiness2(stream, numrounds=10000)
        print('part2', part2)

if __name__ == '__main__':
    main() 