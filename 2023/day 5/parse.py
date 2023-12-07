from map import Map, Mapping

def parse(stream):

    # read seeds
    lineType, lineData = stream.readline().strip().split(':')
    assert lineType == 'seeds'
    seeds = list(map(int, lineData.split()))

    # skip blank line
    stream.readline()

    # read maps
    maps = {}
    while True:

        # extract map type
        line = stream.readline().strip()
        if line:
            mapType, keyword = line.split()
            assert keyword == 'map:'

            # extract the mappings
            mappings = []
            while True:
                line = stream.readline().strip()
                if line:
                    destStart, srcStart, rangeLen = map(int, line.split())
                    assert rangeLen > 0
                    mappings.append(Mapping(destStart, srcStart, rangeLen))
                else:
                    break

            # create new map
            maps[mapType] = Map(mappings)
        else:
            break

    return seeds, maps