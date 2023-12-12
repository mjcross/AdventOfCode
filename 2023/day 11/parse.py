from utils.grid import Grid

def parse(stream):
    stream.seek(0)
    
    # get dimensions of grid
    width = len(stream.readline().strip('\n'))

    height = 1
    while stream.readline():
        height += 1

    # rewind stream and initialise grid
    stream.seek(0)
    emptyCols = set(range(width))
    emptyRow = '.' * width

    rows = []
    for rowNum, rawline in enumerate(stream):
        row = rawline.strip()
        rows.append(row)
        if row == emptyRow:
            # double up empty rows
            rows.append(row)
        # update set of empty cols
        for colNum, c in enumerate(row):
            if c == '#' and colNum in emptyCols:
                emptyCols.remove(colNum)
    
    # expand the empty columns
    expandedRows = []
    for row in rows:
        expandedRow = ''
        for colNum, c in enumerate(row):
            expandedRow += c
            if colNum in emptyCols:
                expandedRow += c
                assert c == '.'
        expandedRows.append(expandedRow)

    return Grid(len(expandedRow), len(expandedRows), expandedRows)


def parse2(stream, expansion):
    """The previous approach isn't going to work when the
       amount of expansion is very large."""
    stream.seek(0)

    # get dimensions of grid
    width = len(stream.readline().strip('\n'))
    height = 1
    while stream.readline():
        height += 1
    stream.seek(0)

    rows = [rawline.strip() for rawline in stream]
    emptyCols = set(range(width)) 
    rowLookup = []  # expanded row index lookup
    emptyRow = '.' * width
    rowNum = 0
    for row in rows:
        rowLookup.append(rowNum)
        if row == emptyRow:
            rowNum += expansion
        else:
            rowNum += 1
        for colNum, c in enumerate(row):    # update list of empty columns
            if c == '#' and colNum in emptyCols:
                emptyCols.remove(colNum)

    # initialise grid using reversed rows so that the Y coords match the lookup
    grid = Grid(width, height, reversed(rows))

    colLookup = []
    expandedColNum = 0
    for colNum in range(width):
        colLookup.append(expandedColNum)
        if colNum in emptyCols:
            expandedColNum += expansion
        else:
            expandedColNum += 1

    return grid, colLookup, rowLookup