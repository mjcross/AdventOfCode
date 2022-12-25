from collections import namedtuple

Cost = namedtuple('Cost', 'ore clay obsidian')
RobotCost = namedtuple('RobotCost', 'ore clay obsidian geode')

class Factory:
    def __init__(self, blueprint)


def part1(stream):
    pass


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
    #    assert result == 'xxxxx', result

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    #with open('input.txt') as stream:
    #    result = part1(stream)
    #    print('part1', result)

    #with open('input.txt') as stream:
    #    print('part2', part2(stream))


if __name__ == '__main__':
    main()