from parse import parse
from map import Span


def part1(stream):
    seeds, maps = parse(stream)
    for mapname in ['seed-to-soil',
                    'soil-to-fertilizer',
                    'fertilizer-to-water',
                    'water-to-light',
                    'light-to-temperature',
                    'temperature-to-humidity',
                    'humidity-to-location']:
        seeds = map(maps[mapname].map, seeds)
    return min(seeds)


def part2(stream):
    seeds, maps = parse(stream)

    # convert seeds to spans
    spans = []
    while seeds:
        spanLen = seeds.pop()
        assert spanLen > 0
        spanStart = seeds.pop()
        spanStop = spanStart + spanLen - 1
        spans.append(Span(spanStart, spanStop))

    newSpans = maps['seed-to-soil'].mapSpans(spans)
    print(spans)
    print(newSpans)
    pass



def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 35, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    #with open('input.txt') as stream:
    #    result = part2(stream)
    #    print(f'part2 {result}')


if __name__ == '__main__':
    main()