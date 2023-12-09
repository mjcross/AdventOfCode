from parse import Race, parse, parse2
from math import sqrt, floor

def part1(stream):
    races = parse(stream)
    margin = 1
    for race in races:
        T, Smax = race.time, race.distance
        tmax = (T + sqrt(T*T - 4*Smax))/2
        tmin = (T - sqrt(T*T - 4*Smax))/2
        ways = floor(tmax) - floor(tmin)
        if tmax == floor(tmax): 
            # incomplete final interval
            ways -= 1
        margin *= ways
    return margin

def part2(stream):
    T, Smax = parse2(stream)
    tmax = (T + sqrt(T*T - 4*Smax))/2
    tmin = (T - sqrt(T*T - 4*Smax))/2
    ways = floor(tmax) - floor(tmin)
    if tmax == floor(tmax):
        # incomplete final interval
        ways -= 1
    return ways


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 288, result

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 71503, result


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