from parse import parse
from tree import Tree, Node
from itertools import cycle
from math import lcm

def part1(stream):
    turnSeq, tree = parse(stream)
    turnIter = cycle(turnSeq)
    node = tree.startNodes[0]
    stepCount = 0
    while node is not tree.endNodes[0]:
        stepCount += 1
        if next(turnIter) == 'L':
            node = node.left
        else:
            node = node.right
    return stepCount


def part2(stream):
    turnSeq, tree = parse(stream)
    cycleLengths = []
    for startNode in tree.startNodes:
        stepCount = 0                   #! it's essential to reset the
        turnIter = cycle(turnSeq)       #! stepcount and the cycle each time
        node = startNode
        while not node.isEndNode:
            stepCount += 1
            if next(turnIter) == 'L':
                node = node.left
            else:
                node = node.right
        cycleLengths.append(stepCount)
    print(cycleLengths)
    return lcm(*cycleLengths)

def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 6, result

    #with open('example2.txt') as stream:
    #    result = part2(stream)
    #    print(f'example2: {result}')
    #    assert result == 6, result


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