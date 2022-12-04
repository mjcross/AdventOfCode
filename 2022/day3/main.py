items = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
assert len(items) == 26 * 2
priority = {item:index+1 for index, item in enumerate(items)}

def part1():
    prioritySum = 0
    with open('input.txt') as inFile:
        for line in inFile:
            compartmentSize = len(line) // 2
            c1 = set(line[compartmentSize:])
            c2 = set(line[:compartmentSize])
            [sharedItem] = c1.intersection(c2)
            prioritySum += priority[sharedItem]
    return prioritySum

def part2():
    prioritySum = 0
    with open('input.txt') as inFile:
        while True:
            r1 = set(inFile.readline().strip())
            r2 = set(inFile.readline().strip())
            r3 = set(inFile.readline().strip())
            if not r1:
                break
            assert r2 and r3
            [sharedItem] = r1.intersection(r2.intersection(r3))
            prioritySum += priority[sharedItem]
    return prioritySum

def main():
    print('part1:', part1())
    print('part2', part2())

if __name__ == '__main__':
    main()