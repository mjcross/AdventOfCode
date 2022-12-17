from array import array
from copy import copy, deepcopy

# globals
valveindex = {}                 # valve name -> index
valvename = []                  # valve nams
valveflowrate = array('B')      # valve flow rates
valvetotalflow = array('I')     # total flow through each valve
valvetunnels = []               # tunnels from each valve
valvetunnelcounts = []          # number of times each tunnel from each valve has been traversed 


def parse(stream):
    """unpck records into global lists"""
    valvetunnelnames = []
 
    index = 0
    for line in stream:

        # unpack record and add to lists
        field = line.split()
        valvename.append(field[1])
        valveflowrate.append(int(field[4].strip(';').split('=')[1]))
        valvetotalflow.append(0)
        valvetunnelnames.append([item.strip(',') for item in field[9:]])
        valvetunnelcounts.append([0 for item in field[9:]])

        # associate name with index
        valveindex[field[1]] = index
        index += 1

    # convert tunnelnames to indices
    for tunnelname in valvetunnelnames:
        valvetunnels.append([valveindex[name] for name in tunnelname])


def pathtotal(timeleft, thisvalve, totalflows, counts):
    print(f'{"." * timeleft}at valve {valvename[thisvalve]} with {timeleft} mins left')

    if timeleft <= 2:
        # no time left to open a valve and get some flow
        # calculate the total flow for this path
        print(f'{"." * (30 - timeleft)}insuffient time to open another valve - path total: {sum(valvetotalflow)}')
        return sum(valvetotalflow)

    # decide whether to open the valve in this room
    if totalflows[thisvalve] == 0 and valveflowrate[thisvalve]:
        # this valve is closed and has a non-zero flow rate
        #! in the general case it /might/ be worth skipping a low quality valve
        timeleft -= 1
        if timeleft > 0:
            totalflows[thisvalve] = timeleft * valveflowrate[thisvalve]
            print(f'{"." * (30 - timeleft)}opened {valvename[thisvalve]} achieving {timeleft} x {valveflowrate[thisvalve]} = {totalflows[thisvalve]}')

    if timeleft >= 3:
        # there is ehough time left to go down a tunnel, open a valve and get some flow
        subpathflows = []
        for tunnelindex, newvalve in enumerate(valvetunnels[thisvalve]):
            # don't go down any tunnel more than twice
            if valvetunnelcounts[thisvalve][tunnelindex] <= 2:
                valvetunnelcounts[thisvalve][tunnelindex] += 1
                print(f'{"." * (30 - timeleft)}trying tunnel {valvename[tunnelindex]} traversal count {valvetunnelcounts[thisvalve][tunnelindex]}')
                subpathflows.append(
                    pathtotal(timeleft - 1, newvalve, copy(valvetotalflow), deepcopy(valvetunnelcounts)))
        
        # tried all the tunnels
        print(f'{"." * (30 - timeleft)}no more tunnels to try! subpathflows {subpathflows} best {max(subpathflows)}')
        return max(subpathflows)

    print(f'{"." * (30 - timeleft)}insufficient time to go down another tunnel! subpathflows {subpathflows} best {max(subpathflows)}')
    return max(subpathflows)


def part1(stream):
    parse(stream)

    timeleft = 30
    return pathtotal(timeleft, valveindex['AA'], copy(valvetotalflow), deepcopy(valvetunnelcounts))

def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream)
        #assert example1 == 'xxxxx', example1

    #with open('example.txt') as stream:
    #    example2 = part2(stream)
    #    assert example2 == 'xxxxx', example2


def main():
    checkexamples()

    #with open('input.txt') as stream:
    #    print('part1', part1(stream))

    #with open('input.txt') as stream:
    #    print('part2', part2(stream))


if __name__ == '__main__':
    main()