def part1(stream):
    pass


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream)
        assert example1 == 'xxxxx', example1

    #with open('example.txt') as stream:
    #    example2 = part2(stream)
    #    assert example2 == 'xxxxx', example2


def main():
    checkexamples()

    #with open('input.txt') as stream:
    #    print('part1', part1(stream))

    #with open('input.txt') as stream:
    #    print('part2', part2(stream))


if __name__ == '__main__':
    main()