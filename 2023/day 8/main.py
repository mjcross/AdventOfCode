from parse import parse
from tree import Tree, Node

def part1(stream):
    turn, tree = parse(stream)
    node = tree.startNodes[0]
    stepCount = 0
    while node is not tree.endNodes[0]:
        stepCount += 1
        if next(turn) == 'L':
            node = node.left
        else:
            node = node.right
    return stepCount


def part2(stream):
    turn, tree = parse(stream)
    nodes = tree.startNodes
    stepCount = 0
    while True:
        #print(nodes)

        # check whether all nodes are endNodes
        for node in nodes:
            if node.isEndNode == False:
                break
        else:
            # done
            return stepCount
        
        # advance all nodes in parallel
        stepCount += 1
        if next(turn) == 'L':
            #nodes = [node.left for node in nodes]
            for i in range(len(nodes)):
                nodes[i] = nodes[i].left
        else:
            #nodes = [node.right for node in nodes]
            for i in range(len(nodes)):
                nodes[i] = nodes[i].right

def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 6, result

    with open('example2.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 6, result


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