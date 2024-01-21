from time import perf_counter

def part1(stream):
    tStart = perf_counter()

    result = None

    tFinish = perf_counter()
    return result, tFinish - tStart


def part2(stream):
    tStart = perf_counter()

    result = None

    tFinish = perf_counter()
    return result, tFinish - tStart


def checkexamples():
    with open('example.txt') as stream:
        result, tSec = part1(stream)
        print(f'example1: {result} ({tSec:0.6f} sec)')
    #    assert result == 'xxxxx', result

    #with open('example.txt') as stream:
    #    result, tSec = part2(stream)
    #    print(f'example2: {result} ({tSec:0.6f} sec)')
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    #with open('input.txt') as stream:
    #    result, tSec = part1(stream)
    #    print(f'part1: {result} ({tSec:0.6f} sec)')

    #with open('input.txt') as stream:
    #    result, tSec = part2(stream)
    #    print(f'part2 {result} ({tSec:0.6f} sec)')


if __name__ == '__main__':
    main()