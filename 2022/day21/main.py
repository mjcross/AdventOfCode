from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from utils.listdelta import delta
from fractions import Fraction
from math import lcm

class Operation(Enum):
    PLUS = lambda x, y: x + y
    MINUS = lambda x, y: x - y
    TIMES = lambda x, y: x * y
    OVER = lambda x, y: x / y
    NONE = None


@dataclass
class Monkey:
    monkey1: Monkey
    monkey2: Monkey
    operation: Operation
    number: int
    monkey1name: str = ''
    monkey2name: str = ''

    @property
    def value(self):
        if self.operation is Operation.NONE:
            return self.number
        else:
            return self.operation(self.monkey1.value, self.monkey2.value)


def parse(stream):
    operations = {
        '+': Operation.PLUS,
        '-': Operation.MINUS,
        '*': Operation.TIMES,
        '/': Operation.OVER
    }
    monkeys = {}
    for line in stream:
        fields = line.split()
        name = fields[0].rstrip(':')
        if len(fields) == 4:
            # todo: add monkey1 and monkey2 links in next pass
            monkey1name = fields[1]
            opcode = fields[2]
            monkey2name = fields[3]
            monkeys[name] = Monkey(None, None, operations[opcode], 0, monkey1name, monkey2name)
        elif len(fields) == 2:
            number = Fraction(fields[1])
            monkeys[name] = Monkey(None, None, Operation.NONE, number)
    for this in monkeys.values():
        if this.operation is not Operation.NONE:
            this.monkey1 = monkeys[this.monkey1name]
            this.monkey2 = monkeys[this.monkey2name]
    return monkeys


def part1(stream):
    monkeys = parse(stream)
    return monkeys['root'].value


def part2(stream):
    monkeys = parse(stream)
    monkeys['root'].operation = Operation.MINUS
    y = monkeys['root']
    x = monkeys['humn']
    values = [y.value for x.number in range(10)]
    deltas = list(delta(values))
    # check the differences are equal
    assert deltas == len(deltas) * [deltas[0]], 'non-linear relationship'
    m = deltas[0]
    c = values[0]
    x.number = -c / m
    assert y.value == 0
    return x.number


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 152

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 301


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print('part1', result)

    with open('input.txt') as stream:
        print('part2', part2(stream))


if __name__ == '__main__':
    main()