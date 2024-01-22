from time import perf_counter
from itertools import combinations, pairwise
from random import seed, sample
from itertools import pairwise
from collections import Counter

from parse import parse
from vector import Vector


def shortestPath(start, end, neighbourDir):
    """Finds the shortest path between two nodes."""
    paths = [[start]]
    visited = {start}
    while paths:
        newPaths = []
        for path in paths:
            visited.add(path[-1])
            for nextStep in neighbourDir[path[-1]]:
                if nextStep == end:
                    path.append(nextStep)
                    return path
                if nextStep not in visited:
                    newPath = path.copy()
                    newPath.append(nextStep)
                    if nextStep == end:
                        return newPath
                    else:
                        newPaths.append(newPath)
        paths = newPaths


def part1(stream):
    nodes, links = parse(stream)
    tStart = perf_counter()

    # build neighbour lists
    for node in nodes:
        node.neighbours = []
    for link in links:
        link.a.neighbours.append(link.b)
        link.b.neighbours.append(link.a)

    # build neighbour directory
    neighbourDir = {node.name: tuple(neighbour.name for neighbour in node.neighbours) for node in nodes}

    # the path between two randomly-chosen nodes traverses a 'bridge' link about 50% of the time
    nSamples = 200
    nodeNames = [node.name for node in nodes]
    pathLinks = []
    for _ in range(nSamples):
        start, end = sample(nodeNames, 2)
        path = shortestPath(start, end, neighbourDir)

        # links traversed by this path
        for pair in pairwise(path):
            pathLinks.append(tuple(sorted(pair)))

    # we expect the bridges to be the most heavily used links
    bridges = [c[0] for c in Counter(pathLinks).most_common(3)]
    print('Bridges:')
    for bridge in bridges:
        print(f'\t{bridge[0]}-{bridge[1]}')

    # remove the bridges
    links = [l for l in links if tuple(sorted([l.a.name, l.b.name])) not in bridges]

    # rebuild neighbour lists
    for node in nodes:
        node.neighbours = []
    for link in links:
        link.a.neighbours.append(link.b)
        link.b.neighbours.append(link.a)

    # rebuild neighbour directory
    neighbours = {node.name: tuple(neighbour.name for neighbour in node.neighbours) for node in nodes}

    # find all nodes linked to node[0]
    group = set()
    newNames = {nodes[0].name}
    while newNames:
        nextNewNames = set()
        for name in newNames:
            group.add(name)
            nextNewNames.update(neighbours[name])
        newNames = nextNewNames - group

    print(f'Groups:\n\t{len(group)}\n\t{len(nodes) - len(group)}')

    result = len(group) * (len(nodes) - len(group))

    tFinish = perf_counter()
    return result, tFinish - tStart


def part2(stream):
    tStart = perf_counter()

    result = None

    tFinish = perf_counter()
    return result, tFinish - tStart


def checkexamples():
    with open('example.txt') as stream:
        result, tSec = part1(stream)
        print(f'example1: {result} ({tSec:0.6f} sec)')
        assert result == 54, result

    #with open('example.txt') as stream:
    #    result, tSec = part2(stream)
    #    print(f'example2: {result} ({tSec:0.6f} sec)')
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result, tSec = part1(stream)
        print(f'part1: {result} ({tSec:0.6f} sec)')

    #with open('input.txt') as stream:
    #    result, tSec = part2(stream)
    #    print(f'part2 {result} ({tSec:0.6f} sec)')


if __name__ == '__main__':
    main()