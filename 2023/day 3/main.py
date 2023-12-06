from utils.streamToArray import streamToArray

def part1(stream):
    a = streamToArray(stream)
    adjacent = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    
    # locate engine parts and look for adjacent strings of digits
    partNumsByCoord = {}
    partsByCoord = {}
    for partIndex, value in enumerate(a._array):
        c = chr(value)
        if not c in '.0123456789':
            partsByCoord[a.index_to_xy(partIndex)] = c

    #! print("parts:", partsByCoord)
            
    # check parts for adjacent part numbers
    for partCoords, partChr in partsByCoord.items():
        partX, partY = partCoords

        #! print("checking part", partChr, "at", partCoords)

        for dX, dY in adjacent:
            lookX = partX + dX
            lookY = partY + dY
            try:
                if chr(a[(lookX, lookY)]).isdigit():
                    # found a digit
                    #! print("\t", chr(a[(lookX, lookY)]), "at", lookX, lookY)

                    # find start of part number
                    while lookX >= 0 and chr(a[(lookX, lookY)]).isdigit():
                        lookX -= 1
                    lookX += 1

                    # ignore part numbers we've already found
                    partNumCoords = (lookX, lookY)
                    if partNumCoords not in partNumsByCoord:
                        #! print("\t\tnew part num starting at", partNumCoords)

                        # read part number
                        partNumStr = ''
                        while lookX < a.width and chr(a[(lookX, lookY)]).isdigit():
                            partNumStr += chr(a[(lookX, lookY)])
                            lookX += 1
                            #! print("\t\t\t", partNumStr)

                        partNumsByCoord[partNumCoords] = int(partNumStr)

            except IndexError:
                pass

    #! print("part numbers:", partNumsByCoord)
    return sum(partNumsByCoord.values())        


def part2(stream):
    a = streamToArray(stream)
    adjacent = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    
    # locate gears and look for adjacent strings of digits
    gearsByCoord = {}
    partNumsByCoord = {}
    for index, value in enumerate(a._array):
        if chr(value) == '*':

            partNumCount = 0
            gearRatio = 1
            gearX, gearY = a.index_to_xy(index)

            #! print("checking gear", gear)

            for dX, dY in adjacent:
                lookX = gearX + dX
                lookY = gearY + dY
                try:
                    if chr(a[(lookX, lookY)]).isdigit():
                        # found a digit
                        #! print("\t", chr(a[(lookX, lookY)]), "at", lookX, lookY)

                        # find start of part number
                        while lookX >= 0 and chr(a[(lookX, lookY)]).isdigit():
                            lookX -= 1
                        lookX += 1

                        # ignore part numbers we've already found
                        partNumCoords = (lookX, lookY)
                        if partNumCoords not in partNumsByCoord:
                            #! print("\t\tnew part num starting at", partNumCoords)

                            # read part number
                            partNumStr = ''
                            while lookX < a.width and chr(a[(lookX, lookY)]).isdigit():
                                partNumStr += chr(a[(lookX, lookY)])
                                lookX += 1
                                #! print("\t\t\t", partNumStr)

                            partNumsByCoord[partNumCoords] = int(partNumStr)

                            gearRatio *= int(partNumStr)
                            partNumCount += 1

                except IndexError:
                    pass

            if partNumCount == 2:
                # valid gears have exactly two adjacent part numbers
                gearsByCoord[(gearX, gearY)] = gearRatio

    #! print(gearsByCoord)
    return sum(gearsByCoord.values())


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 4361, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 467835, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()