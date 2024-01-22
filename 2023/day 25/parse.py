from dataclasses import dataclass
from vector import Vector
from random import seed, randint


@dataclass
class Node:
    name: str
    pos: Vector
    force: Vector
    neighbours: list


@dataclass
class Link:
    a: Node
    b: Node
    
    def __str__(self):
        return f'{self.a.name}-{self.b.name}'
    

def parse(stream) -> (list[Node], list[Link]):

    # initialise the random number generator
    seed()

    # create node index
    nodeIndex = {}
    nodes = []
    stream.seek(0)
    for rawline in stream:
        line = rawline.strip()

        node, subnodes = line.split(':')

        usedCoords = set()
        for name in [node] + subnodes.split():
            if name not in nodeIndex:
                
                # two nodes must not occupy the same location 
                while True:
                    coords=(randint(-100, 100), randint(-100, 100), randint(-100, 100))
                    if coords not in usedCoords:
                        usedCoords.add(coords)
                        break

                newNode = Node(
                    name=name, 
                    pos=Vector(*coords),
                    force=Vector.zero(),
                    neighbours = []
                )
                nodeIndex[name] = newNode
                nodes.append(newNode)

    # create links between nodes
    stream.seek(0)
    links = []
    for rawline in stream:
        line = rawline.strip()

        node, subnodes = line.split(':')

        for subnode in subnodes.split():
            newLink = Link(
                a=nodeIndex[node],
                b=nodeIndex[subnode]
            )
            links.append(newLink)

    return nodes, links
    