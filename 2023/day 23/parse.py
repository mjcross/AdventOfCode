from __future__ import annotations  # solve circular reference btw Link and Node 
from grid import Grid, gridFromstream
from dataclasses import dataclass, field
from typing import Self
from enum import Enum
from warnings import warn

class Direction(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)

    @property
    def symbol(self):
        if self is Direction.N:
            return '^'
        elif self is Direction.E:
            return '>'
        elif self is Direction.S:
            return 'v'
        elif self is Direction.W:
            return '<'
        else:
            raise ValueError
        
    @property
    def reverse(self):
        # reverse direction
        if self is Direction.N:
            return Direction.S
        elif self is Direction.E:
            return Direction.W
        elif self is Direction.S:
            return Direction.N
        elif self is Direction.W:
            return Direction.E
        else:
            raise ValueError


@dataclass
class Path:
    dest: Node
    cost: int

    def __str__(self):
        return f'{self.dest.id}:{self.cost}'


@dataclass
class Node:
    id: int
    paths: list[Path]
    coords: tuple[int, int]

    def __str__(self):
        return f'Node {self.id} (self.x, self.y) paths: {[path.__str__() for path in self.paths]}'


def findNodes(grid: Grid) -> list[Node]:
    nodes = []
    nodeIndex = 0
    for y in reversed(range(0, grid.height)):
        for x in range(0, grid.width):
            if grid[x, y] == '.':
                numClear = 0
                try:
                    for direction in Direction:
                        dx, dy = direction.value
                        if grid[x + dx, y + dy] != '#':
                            numClear += 1

                    if numClear > 2:
                        # found a node
                        nodes.append(Node(nodeIndex, [], (x, y)))
                        nodeIndex += 1

                except IndexError:
                    # we should only go off the map at the start or finish
                    assert y == grid.height - 1 or y == 0
                    nodes.append(Node(nodeIndex, [], (x, y)))
                    nodeIndex += 1
    return nodes


def makeNodePaths(nodes: list[Node], grid: Grid) -> list[Node]:

    # construct directory of nodes by coord
    nodeDir = {node.coords: node for node in nodes}

    # trace paths from each node
    for srcNode in nodes:
        for direction in Direction:
            try:
                currentDirection = direction
                dx, dy = direction.value
                x, y = srcNode.coords
                x += dx
                y += dy
                cost = 1

                while grid[x, y] == '.' or grid[x, y] == currentDirection.symbol:
                    # follow path
                    if (x, y) in nodeDir:
                        # reached another node
                        destNode = nodeDir[(x, y)]
                        if destNode is srcNode:
                            warn('loop detected')
                        # add path to source node
                        srcNode.paths.append(Path(destNode, cost))
                        break   # try next direction from srcNode 
                    else:
                        # take next step along path
                        for newDirection in Direction:
                            if newDirection is not currentDirection.reverse:
                                dx, dy = newDirection.value
                                if grid[x + dx, y + dy] == '.' or grid[x + dx, y + dy] == newDirection.symbol:
                                    currentDirection = newDirection
                                    x += dx
                                    y += dy
                                    cost += 1
                                    break
                        else:
                            break   # dead end - try next direction from srcNode

            except IndexError:
                # paths should only leave the map at the start and finish
                assert srcNode is nodes[0] or srcNode is nodes[-1]
                continue   # try next direction from srcNode

    return nodes


def parse(stream):
    grid = gridFromstream(stream)
    nodes = findNodes(grid)
    makeNodePaths(nodes, grid)
    return nodes


def parse2(stream):
    grid = gridFromstream(stream)

    # remove slopes
    for c in '<>^v':
        coords = grid.findAll(c)
        for coord in coords:
            grid[coord] = '.'

    nodes = findNodes(grid)
    makeNodePaths(nodes, grid)

    return nodes