from utils.array2d import Array2D
from io import StringIO

def getDimensions(stream):
    """Determine the size of a rectangular text 'map' from a text stream.
    Returns (nRows, nCols)."""
    nCols = 0
    for lineNum, rawLine in enumerate(stream):
        line = rawLine.strip()

        # check each row has the same number of columns
        if nCols == 0:
            nCols = len(line)
        else:
            assert nCols == len(line)

    # rewind the stream 
    stream.seek(0)

    # the number of rows is 1 + the index of the final row
    return (lineNum + 1, nCols)


def streamToArray(stream):
    """Create a 2D array from a text stream.
    Returns the 2D array."""
    # get the number of colums and rows
    nRows, nCols = getDimensions(stream)

    # create a blank aray of the correct size
    a = Array2D("B", 0, nCols-1, 0, nRows-1)

    # populate the array
    for lineNum, rawLine in enumerate(stream):
        y = nRows - lineNum - 1
        rowStr = rawLine.strip()
        for x, colChar in enumerate(rowStr):
            a[x, y] = ord(colChar)

    return a


def main():
    example = StringIO("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""")
    print("Dimensions:", getDimensions(example), "rows / cols")
    a = streamToArray(example)
    print(a.as_chars())

if __name__ == '__main__':
    main()