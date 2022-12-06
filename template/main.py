def part1():
    pass


def part2():
    pass


def checkexamples():
    examples = [
    ]
    for data, answer in examples:
        assert part1(data) == answer[0]
        assert part2(data) == answer[1]


def main():
    checkexamples()
    with open(input.txt) as infile:
        print(part1())
        print(part2())

if __name__ == '__main__':
    main()