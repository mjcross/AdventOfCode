from collections import deque
from collections import namedtuple
import sys
import pprint

assert sys.version_info >= (3, 7), 'Needs Python 3.7 to maintain insertion order of dict keys'
pp = pprint.PrettyPrinter(indent=4)

Stack = namedtuple('Stack', ['col', 'dq'])

def readstacks(file):
    lines = []
    while True:
        line = file.readline()
        if not line.rstrip():
            break
        lines.append(line)

    header = lines.pop()
    stacknames = header.split()
    stacks = {
        name: Stack(col=header.index(name), dq=deque())
        for name in stacknames
    }

    for line in lines:
        for name, stack in stacks.items():
            box = line[stack.col].rstrip()
            if box:
                stack.dq.appendleft(box)

    return stacks


def movestacks(file, stacks):
    for line in file:
        fields = line.lower().split()
        numboxes = int(fields[fields.index('move') + 1])
        fromstack = stacks[fields[fields.index('from') + 1]]
        tostack = stacks[fields[fields.index('to') + 1]]
        for box in range(numboxes):
            tostack.dq.append(fromstack.dq.pop())
    return stacks


def movestacks9001(file, stacks):
    for line in file:
        fields = line.lower().split()
        numboxes = int(fields[fields.index('move') + 1])
        fromstack = stacks[fields[fields.index('from') + 1]]
        tostack = stacks[fields[fields.index('to') + 1]]
        boxes = [fromstack.dq.pop() for box in range(numboxes)]
        boxes.reverse()
        tostack.dq.extend(boxes)
    return stacks


def part1():
    with open('input.txt') as inFile:
        stacks = readstacks(inFile)
        stacks = movestacks(inFile, stacks)
        return ''.join([stacks[name].dq.pop() for name in stacks.keys()])


def part2():
    with open('input.txt') as inFile:
        stacks = readstacks(inFile)
        stacks = movestacks9001(inFile, stacks)
        return ''.join([stacks[name].dq.pop() for name in stacks.keys()])


def main():
    print('part1', part1())
    print('part2', part2())

if __name__ == '__main__':
    main()