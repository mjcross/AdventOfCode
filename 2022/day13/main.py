from enum import Enum

class Result(Enum):
    RIGHT = True
    NOTRIGHT = False
    UNDECIDED = 2


class Packet:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Packet({self.value})'

    def __lt__(self, other):
        result = compare(self.value, other.value)

        if result == Result.NOTRIGHT:
            return True
        elif result == Result.RIGHT:
            return False
        else:
            raise ValueError(f'{self} __lt__ {other} gave {result}')

    def __eq__(self, other):
        return self.value == other.value


def compare(left, right):
    if type(left) is int and type(right) is int:
        if left < right:
            return Result.RIGHT
        elif left > right:
            return Result.NOTRIGHT 
        else:
            return Result.UNDECIDED

    elif type(left) is int and type(right) is list:
        return compare([left], right)

    elif type(left) is list and type(right) is int:
        return compare(left, [right])

    elif type(left) is list and type(right) is list:
        for a, b in zip(left, right):
            elementresult = compare(a, b)
            if elementresult == Result.RIGHT:
                return Result.RIGHT
            elif elementresult == Result.NOTRIGHT:
                return Result.NOTRIGHT
            elif elementresult == Result.UNDECIDED:
                pass
            else:
                raise ValueError(elementresult)
        if len(right) < len(left):
            return Result.NOTRIGHT
        elif len(left) < len(right):
            return Result.RIGHT
        else:
            return Result.UNDECIDED

    else:
        raise ValueError(left, right)



def parse(stream):
    pairs = []
    while True:
        pair = []
        exec('pair.append(' + stream.readline().strip() + ')')
        exec('pair.append(' + stream.readline().strip() + ')')
        pairs.append(pair)
        if not stream.readline():
            break
    return pairs
   

def part1(stream):
    pairnumsum = 0
    pairs = parse(stream)
    for pairnum, pair in enumerate(pairs, start=1):
        left, right = pair[0:2]
        result = compare(left, right)
        if result == Result.RIGHT:
            pairnumsum += pairnum
    return pairnumsum


def part2(stream):
    pairs = parse(stream)
    packets = []
    for pair in pairs:
        for packet in pair:
            packets.append(Packet(packet))
    d1 = [[2]]
    d2 = [[6]]
    packets.append(Packet(d1))
    packets.append(Packet(d2))
    packets.sort(reverse=True)
    return (1 + packets.index(Packet(d1))) * (1 + packets.index(Packet(d2)))
    

def checkexamples():
    with open('example.txt') as stream:
        example1 = part1(stream)
        assert example1 == 13, example1

    with open('example.txt') as stream:
        example2 = part2(stream)
        assert example2 == 140, example2


def main():
    checkexamples()

    with open('input.txt') as stream:
        print('part1', part1(stream))

    with open('input.txt') as stream:
        print('part2', part2(stream))


if __name__ == '__main__':
    main()