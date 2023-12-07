from parse import parse
from map import Span


def part1(stream):
    seeds, maps = parse(stream)
    for mapName in ['seed-to-soil',
                    'soil-to-fertilizer',
                    'fertilizer-to-water',
                    'water-to-light',
                    'light-to-temperature',
                    'temperature-to-humidity',
                    'humidity-to-location']:
        seeds = map(maps[mapName].map, seeds)
    return min(seeds)


def part2(stream):
    # for part(ii) we must interpret pairs of "seed numbers" as (start, len)
    seeds, maps = parse(stream)

    # convert seed numbers into 'Span(first, last)'
    spans = []
    while seeds:
        spanLen = seeds.pop()
        assert spanLen > 0
        spanStart = seeds.pop()
        spanStop = spanStart + spanLen - 1
        spans.append(Span(spanStart, spanStop))

    # apply the maps to the spans
    for mapName in ['seed-to-soil',
                    'soil-to-fertilizer',
                    'fertilizer-to-water',
                    'water-to-light',
                    'light-to-temperature',
                    'temperature-to-humidity',
                    'humidity-to-location']:
        spans = maps[mapName].mapSpans(spans)
    
    # the puzzle asks us to find the lowest location number
    lowestLocation = None
    for span in spans:
        if lowestLocation is None or span.start < lowestLocation:
            lowestLocation = span.start
    return lowestLocation


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 35, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 46, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()