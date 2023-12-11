from grid import Grid

def parse(stream):
    # get dimensions of grid
    width = len(stream.readline().strip('\n'))

    height = 1
    while stream.readline():
        height += 1

    # rewind stream and initialise grid
    stream.seek(0)
    return Grid(width, height, [line.strip('\n') for line in stream])
