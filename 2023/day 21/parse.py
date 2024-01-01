from grid import Grid, gridFromstream

def parse(stream):
    stream.seek(0)
    grid = gridFromstream(stream)
    start = grid.find('S')
    grid[start] = '.'

    return grid, start