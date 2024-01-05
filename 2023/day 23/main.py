from parse import parse, parse2, Node
from time import perf_counter


def exploreFromNode(
        startNode: Node, 
        startCost: int, 
        endNode: Node,
        visited: list[Node], 
        highestCost: list[int]):
    """Makes a recursive depth-first search of the graph
    to identify the highest cost route without re-visiting 
    any node. Records in `highestCost` the highest cost that
    has currently been found to reach each node.
    """
    
    visited.append(startNode)
    highestCost[startNode.id] = startCost
    if startNode is endNode:
        return

    for path in startNode.paths:
        if path.dest in visited:
            # can't re-visit a node
            continue

        if highestCost[path.dest.id] > startCost + path.cost:
            # no point taking an inferior route
            continue

        exploreFromNode(
            startNode=path.dest,
            startCost=startCost + path.cost,
            endNode=endNode,
            visited=visited.copy(),
            highestCost=highestCost
        )

    return


def exploreFromNode2(
        startNode: Node, 
        startCost: int, 
        endNode: Node,
        visited: list[Node], 
        highestCost: list[int]):
    """Makes a recursive depth-first search of the graph
    to identify the highest cost route without re-visiting 
    any node. Records in `highestCost` the highest cost that
    has currently been found to reach each node.
    This version does a full search to allow loops in the graph.
    """
    
    visited.append(startNode)
    highestCost[startNode.id] = max(highestCost[startNode.id], startCost)
    if startNode is endNode:
        return

    for path in startNode.paths:
        if path.dest in visited:
            # can't re-visit a node
            continue

        exploreFromNode2(
            startNode=path.dest,
            startCost=startCost + path.cost,
            endNode=endNode,
            visited=visited.copy(),
            highestCost=highestCost
        )

    return


def part1(stream):
    tStart = perf_counter()
    nodes = parse(stream)

    # optimise search by sorting node paths in descending order of cost
    for node in nodes:
        node.paths.sort(key=lambda path: path.cost, reverse=True) 

    # recursively find the highest cost to reach each node
    highestCost = [0] * len(nodes)
    exploreFromNode(
        startNode=nodes[0],
        startCost=0,
        endNode=nodes[-1],
        visited=[],
        highestCost=highestCost
    )

    tFinish = perf_counter()

    executionSec = tFinish - tStart
    return highestCost[-1], executionSec


def part2(stream):
    tStart = perf_counter()
    nodes = parse2(stream)

    # optimise search by sorting node paths in descending order of cost
    for node in nodes:
        node.paths.sort(key=lambda path: path.cost, reverse=True) 

    # recursively find the highest cost to reach each node
    highestCost = [0] * len(nodes)
    exploreFromNode2(
        startNode=nodes[0],
        startCost=0,
        endNode=nodes[-1],
        visited=[],
        highestCost=highestCost
    )

    tFinish = perf_counter()

    executionSec = tFinish - tStart
    return highestCost[-1], executionSec


def checkexamples():
    with open('example.txt') as stream:
        result, tSec = part1(stream)
        print(f'example1: {result} ({tSec:0.6f} sec)')
        assert result == 94, result

    with open('example.txt') as stream:
        result, tSec = part2(stream)
        print(f'example2: {result} ({tSec:0.6f} sec)')
        assert result == 154, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result, tSec = part1(stream)
        print(f'part1: {result} ({tSec:0.6f} sec)')

    with open('input.txt') as stream:
        result, tSec = part2(stream)
        print(f'part2 {result} ({tSec:0.6f} sec)')


if __name__ == '__main__':
    main()