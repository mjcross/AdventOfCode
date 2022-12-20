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
from itertools import permutations, product
from copy import copy
import timeit

debug = 0

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


def topcut2(locations, flowtotal, cutsize, time, leasthops, valvesleft, paths, arrivaltimes, numunopened):
    """Recursively explore the top 'cutsize' moves with several players, and return the best score."""

    # initialise time left and best flow achieved so far
    timeleft = 30 - time
    bestflowtotal = flowtotal

    # allow for not having to open the first valve
    if locations[0].name == 'AA':
        arrivaltimes=[arrivaltime - 1 for arrivaltime in arrivaltimes]

    while True:
        if debug >= 2:
            print(f'\n=== Time {time} ({timeleft} mins left, valves left [{" ".join([valve.name for valve in valvesleft])}]) ===')
            for playernum, (arrivaltime, location) in enumerate(zip(arrivaltimes, locations)):
                print(f'player {playernum}', end=' ')
                if time < arrivaltime:
                    print(f'en route to {location.name}, arriving at time {arrivaltime}')
                elif time == arrivaltime:
                    print(f'arrived at {location.name} and started opening valve')
                elif time == arrivaltime + 1:
                    print(f'ready to move at {location.name}')
                else:
                    print(f'standing idle at {location.name}')

        # manage valve openings

        justopened = None
        for playernum, (location, arrivaltime) in enumerate(zip(locations, arrivaltimes)):
            if time == arrivaltime + 1:
                # a player has just finished opening a valve
                if location.flowrate > 0 and timeleft >= 1 and location != justopened:
                    flowtotal += timeleft * location.flowrate
                    justopened = location    # avoid race condition
                    numunopened -= 1
                    if debug >= 2:
                        print(
                            f'player {playernum} finished opening {location.name} with {timeleft} mins left '
                            f'({location.flowrate} x {timeleft} min = {location.flowrate * timeleft:3d}) new total {flowtotal})')
                    if numunopened == 0:
                        break

        # check whether we've finished this attempt
        if timeleft <= 1 or numunopened == 0:
            if debug >= 1:
                print(f'>>> {paths} = {flowtotal}\t({timeleft} mins left, {numunopened} un-opened valves) <<<')
            return max(flowtotal, bestflowtotal)

        # choose next destinations for available players
        playercandidates = []
        for location, arrivaltime in zip(locations, arrivaltimes):
            candidates = []
            if time >= arrivaltime + 1:
                # player has finished opening a valve and is ready to move
                #   - identify top few destinations, based on time to get there and open the valve
                candidates = [(valve, valve.flowrate * (timeleft - (1 + leasthops[location, valve]))) for valve in valvesleft]
                candidates.sort(key=lambda x: x[1], reverse=True)
                candidates = candidates[:cutsize]
            playercandidates.append(candidates)

        if debug >= 2:
            for playernum, candidates in enumerate(playercandidates):
                print(f'\tplayer {playernum} candidates:', end=' ')
                if candidates:
                    for candidate in candidates:
                        print(f'\t{candidate[0].name} ({candidate[1]:3d})', end='')
                    print()
                else:
                    print('\tn/a')

        # recursively try the top few destinations for the available player(s)
        #   - note that playercandidates[] entries are only set for available players

        if playercandidates[0] and playercandidates[1]:
            # both players are ready to move - explore all combinations of their two lists (this may be a bit OTT)
            #! is there a slight possibility that both players are available, but there's only one valve left?
            for candidate in product(*playercandidates):
                dest0, flow0 = candidate[0]
                dest1, flow1 = candidate[1]
                if dest0 != dest1 or (len(playercandidates[0]) == 1 and len(playercandidates[1]) == 1):
                    # don't send both players to the same destination unless there are no other options
                    if debug >= 2:
                        print(f'sending player 0 to {dest0.name}({flow0}/{leasthops[locations[0], dest0]} hops) and player 1 to {dest1.name}({flow1}/{leasthops[locations[1], dest1]} hops)')

                    newvalvesleft = copy(valvesleft)
                    newvalvesleft.remove(dest0)
                    if dest1 != dest0:
                        newvalvesleft.remove(dest1)

                    newarrivaltimes = [
                        time + leasthops[locations[0], dest0],
                        time + leasthops[locations[1], dest1]
                    ]

                    result = topcut2(
                        locations=[dest0, dest1],
                        flowtotal=flowtotal,
                        cutsize=cutsize,
                        time=1 + min(newarrivaltimes),
                        leasthops=leasthops,
                        valvesleft=newvalvesleft,
                        paths=[paths[0] + ' ' + dest0.name, paths[1] + ' ' + dest1.name],
                        arrivaltimes=newarrivaltimes,
                        numunopened=numunopened
                    )

                    bestflowtotal = max(bestflowtotal, result)

            # tried all the options
            return bestflowtotal

        elif playercandidates[0]:
            # only player0 is available
            for candidate in playercandidates[0]:
                dest0, flow0 = candidate
                if debug >= 2:
                    print(f'sending player 0 to {dest0.name}({flow0}/{leasthops[locations[0], dest0]} hops)')

                newvalvesleft = copy(valvesleft)
                newvalvesleft.remove(dest0)

                newarrivaltimes = [
                    time + leasthops[locations[0], dest0],
                    arrivaltimes[1]
                ]

                result = topcut2(
                    locations=[dest0, locations[1]],
                    flowtotal=flowtotal,
                    cutsize=cutsize,
                    time=1 + min(newarrivaltimes),
                    leasthops=leasthops,
                    valvesleft=newvalvesleft,
                    paths=[paths[0] + ' ' + dest0.name, paths[1]],
                    arrivaltimes=newarrivaltimes,
                    numunopened=numunopened
                )

                bestflowtotal = max(bestflowtotal, result)

            # tried all the options
            return bestflowtotal

        elif playercandidates[1]:
            # only player1 is available
            for candidate in playercandidates[1]:
                dest1, flow1 = candidate
                if debug >= 2:
                    print(f'sending player 1 to {dest1.name}({flow1}/{leasthops[locations[1], dest1]} hops)')

                newvalvesleft = copy(valvesleft)
                newvalvesleft.remove(dest1)

                newarrivaltimes = [
                    arrivaltimes[0],
                    time + leasthops[locations[1], dest1],
                ]

                result = topcut2(
                    locations=[locations[0], dest1],
                    flowtotal=flowtotal,
                    cutsize=cutsize,
                    time=1 + min(newarrivaltimes),
                    leasthops=leasthops,
                    valvesleft=newvalvesleft,
                    paths=[paths[0], paths[1] + ' ' + dest1.name],
                    arrivaltimes=newarrivaltimes,
                    numunopened=numunopened
                )

                bestflowtotal = max(bestflowtotal, result)

            # tried all the options
            return bestflowtotal

        else:
            # neither player was ready to move
            if debug >= 2:
                print('neither player is ready to move')
            time += 1
            timeleft -= 1


def part1(stream):
    valvedict = parse(stream)
    start = valvedict['AA']
    valves = [valve for valve in valvedict.values() if valve.flowrate]
    leasthops = hoptable([start] + copy(valves))
    return topcut(
        current=start, 
        flowtotal=0, 
        cutsize=8, 
        timeleft=30, 
        leasthops=leasthops, 
        valvesleft=valves, 
        path=[])


def part2(stream, cutsize):
    valvedict = parse(stream)
    start = valvedict['AA']
    valves = [valve for valve in valvedict.values() if valve.flowrate]
    leasthops = hoptable([start] + copy(valves))
    return topcut2(
        locations=[start, start],
        flowtotal=0,
        cutsize=cutsize,
        time=4,
        leasthops=leasthops,
        valvesleft=valves,
        paths=[start.name, start.name],
        arrivaltimes=[4, 4],
        numunopened=len(valves))


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream)
        print(f'example1 = {example1}')
        assert example1 == 1651, example1

    with open('example.txt') as stream:
        example2 = part2(stream, cutsize = 3)
        print(f'example2 = {example2}')
        assert example2 == 1707, example2


def main():
    checkexamples()

    with open('input.txt') as stream:
        start = timeit.default_timer()
        print('part1', part1(stream))
        stop = timeit.default_timer()
        print(f'took {stop-start:.2f} sec')
   
    with open('input.txt') as stream:
        start = timeit.default_timer()
        print('part2', part2(stream, cutsize=6))
        stop = timeit.default_timer()
        print(f'took {stop-start:.2f} sec')

if __name__ == '__main__':
    main()