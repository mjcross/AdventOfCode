def part1(stream):
    pass


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
    #    assert result == 'xxxxx', result

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    print(f'example2: {result}')
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    #with open('input.txt') as stream:
    #    result = part1(stream)
    #    print(f'part1 {result}')

    #with open('input.txt') as stream:
    #    result = part2(stream)
    #    print(f'part2 {result}')


if __name__ == '__main__':
    main()