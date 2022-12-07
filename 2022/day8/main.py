def part1():
    pass


def part2():
    pass


def checkexamples():
    examples = [
    ]
    for data, answer in examples:
        if part1(data) == answer[0]:
            print("example 1 *** PASS ***")
        else:
            print('example 1 *** FAIL ***')
        if part2(data) == answer[1]:
             print("example 2 *** PASS ***")
        else:
            print('example 2 *** FAIL ***')


def main():
    checkexamples()
    with open('input.txt') as infile:
        print(part1())
        print(part2())

if __name__ == '__main__':
    main()