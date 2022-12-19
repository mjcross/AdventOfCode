"""
Observations about the puzzle
=============================
1) The optimum route involves navigating by the shortest path between nodes
where you want to DO something (in this case, turn on a valve). So ignore the
zero-flowrate valves and just navigate between the useful ones.
2) The cost of the 'cheapest' route between nodes doesn't change, so you can
precompute it.
3) Unfortunately the puzzle has 15 non-zero nodes so there are 10^12 different
ways to visit them all. This means ANY approach that involves checking every 
possible sequence (even really fast) is doomed. 
4) Some kind of intelligent approach (or at least a heuristic) is therefore
needed. 
    - One suggestion is to limit the amount of 'look-ahead' to a given depth, 
      and choose the best option based on that.
    - Another idea is to give every possible next destination a score based
      on benefit (which in this case depends on time) minus cost
    - An observation is that the 'high level' structure of the graph MATTERS.
      Cul-de-sacs demand a different strategy to loops.
"""

from utils.route import Node, leasthops, hoptable, showhoptable
from itertools import permutations
from copy import copy
import timeit

debug = 1

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


def topcut(current, flowtotal, cutsize, timeleft, leasthops, valvesleft, path):
    """Recursively explore the top 'cutsize' moves and return the best score."""
    path.append(current.name)
 
    if current.flowrate > 0 and timeleft > 1:
        # open valve at current location
        timeleft -= 1
        flowtotal += timeleft * current.flowrate
        if debug >= 2:
            print(f'opened {current.name} rate {current.flowrate:2d} with {timeleft:2d} mins left = {current.flowrate * timeleft:3d} (total {flowtotal})')

    if timeleft <= 1 or not valvesleft:
        # out of time or all valves open
        if debug >= 2:
            print(f'{" ".join(path)} = {flowtotal}\t({timeleft} mins left, {len(valvesleft)} valves left)\n')
        return flowtotal
    else:
        # identify best options for next step
        candidates = [(valve, valve.flowrate * (timeleft - leasthops[current, valve] - 1)) for valve in valvesleft]
        candidates.sort(key=lambda x: x[1], reverse=True)
        candidates = candidates[:cutsize]

        bestflowtotal = flowtotal
        for nextvalve, flow in candidates:
            newvalvesleft = copy(valvesleft)
            newvalvesleft.remove(nextvalve)
            newflowtotal = topcut(
                current=nextvalve, 
                flowtotal=flowtotal, 
                cutsize=cutsize, 
                timeleft=timeleft - leasthops[current, nextvalve],
                leasthops=leasthops, 
                valvesleft=newvalvesleft,
                path = copy(path))

            bestflowtotal = max(newflowtotal, bestflowtotal)

        return bestflowtotal


def part1(stream):
    valvedict = parse(stream)
    start = valvedict['AA']
    valves = [valve for valve in valvedict.values() if valve.flowrate]
    leasthops = hoptable([start] + copy(valves))
    return topcut(current=start, flowtotal=0, cutsize=8, timeleft=30, leasthops=leasthops, valvesleft=valves, path=[])


def part1exhaust(stream):
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
        start = timeit.default_timer()
        print('part1', part1(stream))
        stop = timeit.default_timer()
        print(f'took {stop-start:.2f} sec')

    #with open('input.txt') as stream:
    #    print('part2', part2(stream))


if __name__ == '__main__':
    main()