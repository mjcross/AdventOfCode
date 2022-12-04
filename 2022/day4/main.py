def sections(rangestr):
    first, last = rangestr.split('-')
    return set(range(int(first), int(last) + 1))

def main():
    with open('input.txt') as inFile:
        numsubsets = 0
        numintersections = 0
        for line in inFile:
            s0, s1 = [sections(range) for range in line.strip().split(',')]
            if s0.issubset(s1) or s1.issubset(s0):
                numsubsets += 1
            if s0.intersection(s1):
                numintersections += 1
        print('subsets', numsubsets)
        print('intersections', numintersections)

if __name__ == '__main__':
    main()