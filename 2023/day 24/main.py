from time import perf_counter
from itertools import combinations
from fractions import Fraction

from parse import parse, Body
from vector import Vector

def part1(stream, xyMin, xyMax):
    stones = parse(stream)
    tStart = perf_counter()
    
    result = 0
    for h1, h2 in combinations(stones, 2):
        determinant = h1.v.y * h2.v.x - h1.v.x * h2.v.y
        if determinant == 0:
            # parallel lines
            continue
        else:
            lamda = Fraction(
                (h1.p0.x - h2.p0.x) * h2.v.y - (h1.p0.y - h2.p0.y) * h2.v.x,             
                determinant)
            if lamda < 0:
                # in the past for h1
                continue

            mu = Fraction(
                (h1.p0.x - h2.p0.x) * h1.v.y - (h1.p0.y - h2.p0.y) * h1.v.x,
                determinant)
            if mu < 0:
                # in the past for h2
                continue

        x = h1.p0.x + lamda * h1.v.x
        y = h1.p0.y + lamda * h1.v.y

        if xyMin <= x <= xyMax and xyMin <= y <= xyMax:
            result += 1

    tFinish = perf_counter()
    return result, tFinish - tStart


def part2(stream):
    h_orig = parse(stream)
    tStart = perf_counter()

    # *** convert to relative frame with h[0] stationary at the origin ***
    print('\n--- frame relative to h0 ---')

    # adjust everything relative to the first hailstone
    ref = h_orig[0]
    h = [body - ref for body in h_orig]

    # identify the plane that contains the origin (now h0) and the line h1
    n = h[1].v.cross(h[1].p0)   # the plane must contain the vectors h1.vec and (h1 - 0).p0
                                # p.n = 0 because the plane contains the origin
    print('normal to plane h0, h1', n, sep='\t')

    # check that the plane contains h1
    assert h[1].at_time(0).dot(n) == 0
    assert h[1].at_time(1).dot(n) == 0

    # find when and where the plane intersects h2 and h3
    t2 = Fraction(-h[2].p0.dot(n), h[2].v.dot(n))
    t3 = Fraction(-h[3].p0.dot(n), h[3].v.dot(n))
    p2 = h[2].at_time(t2)
    p3 = h[3].at_time(t3)
    print(f'plane intersects h2', f'time {t2} position {p2}', sep='\t')
    print(f'plane intersects h3', f'time {t3} position {p3}', sep='\t')

    # calculate the velocity of the rock
    dp = p3 - p2
    dt = t3 - t2
    v = Vector(Fraction(dp.x, dt), Fraction(dp.y, dt), Fraction(dp.z, dt))
    print('velocity of rock', v, sep='\t')

    # extrapolate back to the initial position of the rock
    p0 = p2 - v * t2
    print('initial pos of rock', p0, sep='\t')

    rock = Body(p0, v)

    # *** return to absolute frame ***
    print('\n--- absolute frame ---')

    rock += ref
    print('velocity of rock', rock.v, sep='\t')
    print('initial pos of rock', rock.p0, sep='\t')
    print()


    result = sum([*rock.p0])
    tFinish = perf_counter()
    return result, tFinish - tStart


def checkexamples():
    with open('example.txt') as stream:
        result, tSec = part1(stream, 7, 27)
        print(f'example1: {result} ({tSec:0.6f} sec)')
        assert result == 2, result

    with open('example.txt') as stream:
        result, tSec = part2(stream)
        print(f'example2: {result} ({tSec:0.6f} sec)')
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result, tSec = part1(stream, 200_000_000_000_000, 400_000_000_000_000)
        print(f'part1: {result} ({tSec:0.6f} sec)')

    with open('input.txt') as stream:
        result, tSec = part2(stream)
        print(f'part2 {result} ({tSec:0.6f} sec)')


if __name__ == '__main__':
    main()