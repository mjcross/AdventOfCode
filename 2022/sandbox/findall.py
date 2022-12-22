def findall(needle, haystack):
    start = 0
    positions = []
    while True:
        pos = haystack.find(needle, start)
        if pos == -1:
            return positions
        else:
            positions.append(pos)
            start = pos + len(needle)


def main():
    #                    0         1         2
    #                    0123456789012345678901
    print(findall('at', 'the cat sat on the mat'))


if __name__ == '__main__':
    main()