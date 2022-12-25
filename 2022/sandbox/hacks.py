from copy import copy

def pathstr(path):
    sums = []
    for multiplier, number in enumerate(path, start=1):
        if number:
            sums.append(f'{number}x{multiplier}')
    return ' + '.join(sums)


def make(target, multiplier, path):
    """returns a list of NEW solution paths found"""
    #print(f'trying to make {target} with x{multiplier} and above ({pathstr(path)})')

    if target == 0:
        #print(f'\ttarget achieved\nADDING {pathstr(path)}')
        return([path])

    if target < multiplier:
        # not possible - no further solutions
        #print('\tnot possible')
        return []

    elif target == multiplier:
        # only one further solution
        #print(f'\t\tonly one way to make {target} with x{multiplier} and above\nADDING {pathstr(path + [1])}')
        return [path + [1]]

    else:
        newsolutions = []
        maxnum = target // multiplier      # e.g. we have to make 7 using x2 ... can't be more than 7 // 2 = 3
        #print(f'\tmaxnum {maxnum} multiplier {multiplier} target {target} path {path}')
        for number in range(maxnum + 1):
            #print(f'\tin the FOR loop: trying {number}x{multiplier}')
            newsolutions += make(
                target=target - number * multiplier, 
                multiplier=multiplier + 1,
                path=path + [number])
        return newsolutions


def main():
    found = make(target=7, multiplier=1, path=[])
    print()
    for path in found:
        print('7 =', pathstr(path))


if __name__ == '__main__':
    main()