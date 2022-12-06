def delta(seq):
    previtem = seq[0]
    for thisitem in seq[1:]:
        yield thisitem - previtem
        previtem = thisitem


def windows(seq, size):
    i = 0
    while i + size <= len(seq):
        yield(seq[i: i + size])
        i += 1


def numincreases(seq):
    return sum(delta > 0 for delta in delta(seq))


def part1(seq):
    return numincreases(seq)


def part2(seq):
    return numincreases([sum(window) for window in windows(seq, 3)])


def main():
    tests = [
        ((199, 200, 208, 210, 200, 207, 240, 269, 260, 263), (7, 5))]

    for testdata, answer in tests:
        assert part1(testdata) == answer[0]
        assert part2(testdata) == answer[1]

    with open('input.txt') as infile:
        depthdata = [int(depth) for depth in infile.readlines()]
        print(part1(depthdata))
        print(part2(depthdata))

if __name__ == '__main__':
    main()