"""
Observations about the puzzle
=============================
1) The optimal route often involves passing through a room without stopping to
turn on a slow valve
2) Before starting to solve the graph, cull out all zero-rated rooms with only
one way in and one way out ('transit nodes')... except the start node!
3) Do NOT try to find the optimal route by trying every possible 30min path 
through the graph. Instead, pick the next sensible destination (a room with a 
turn-on-able valve); travel by the lowest cost route, without stopping, and
turn on the valve. You can then exhaust over all possible sequences of valves.
4) The cheapest route between any pair of nodes without stopping doesn't
change, so it can be pre-computed.
5) Heuristics like not going down blind alleys once, only traversing tunnels
once in each direction etc appear to be negated by the puzzle mechanic. I
think you're better off doing least-cost navigation between chosen nodes.
"""

from utils.route import Node, leasthops, hoptable, showhoptable
from itertools import permutations
from copy import copy

debug = 3

class Valve(Node):
    def __init__(self, name, flowrate, edges):
        self.name = name
        self.flowrate = flowrate
        self.edges = edges

    def __repr__(self):
        return (
            f"Valve(name='{self.name}'"
            f', flowrate={self.flowrate:2d}'
            f', tunnels={[edge.name for edge in self.edges]})')


def parse(stream):
    """Takes a file-type object and returns a dictionary of {name: Valve} pairs."""
    valvedict = {}
    for line in stream:
        # create node from line of text like:
        #   "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
        field = line.split()
        name = field[1]
        flowrate = int(field[4].split('=')[-1].strip(';'))
        edges = [
            name.strip(',')
            for name in field[9:]]
        valvedict[name] = Valve(name=name, flowrate=flowrate, edges=edges)
    # link edges to nodes
    for valve in valvedict.values():
        valve.edges = [valvedict[edge] for edge in valve.edges]
    return valvedict


def part1(stream):
    valvedict = parse(stream)
    if debug >= 3:
        for name, valve in valvedict.items():
            print(f'name: {name} valve: {valve}')

    # select start point and valves with non-zero flowrates
    start = valvedict['AA']
    valves = [valve for valve in valvedict.values() if valve.flowrate]
    if debug >= 2:
        for valve in valves:
            print(valve)

    # pre-calculate hops between valves
    leasthops = hoptable([start] + copy(valves))
    if debug >= 1:
        showhoptable(leasthops)

    bestflow = 0
    for route in permutations(valves):
        nodelist = list(route)
        current = start
        timeleft = 30
        flow = 0
        while nodelist and timeleft > 0:
            # go down tunnel
            dest = nodelist.pop()
            timeleft -= leasthops[(current, dest)]
            current = dest
            if debug >=3:
                print(f'Arrive at {current.name} with {timeleft} min left', end='')
            # turn on valve if there's time
            timeleft -= 1
            if timeleft > 0:
                flow += current.flowrate * timeleft
                if debug >=3:
                    print(f'\topened valve with flowrate {current.flowrate:2d} with {timeleft} min left', end='')
                    print(f'\tflow = {current.flowrate * timeleft:3d}, total {flow}')
        bestflow = max(bestflow, flow)
        if debug >=2:
            print(f'route: {[dest.name for dest in route]} flow {flow} best {bestflow}')
    return bestflow


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream)
        assert example1 == 1651, example1

    #with open('example.txt') as stream:
    #    example2 = part2(stream)
    #    assert example2 == 'xxxxx', example2


def main():
    checkexamples()

    with open('input.txt') as stream:
        print('part1', part1(stream))

    #with open('input.txt') as stream:
    #    print('part2', part2(stream))


if __name__ == '__main__':
    main()