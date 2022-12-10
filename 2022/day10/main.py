from enum import Enum

class State(Enum):
    Fetch = 0
    Adding = 1

class CPU:
    def __init__(self, state=State.Fetch, x=1, v=0):
        self.state = state
        self.x = x
        self.v = v

    def __repr__(self):
        return f'CPU(state:{self.state.name}, x:{self.x}, v:{self.v})'

    def run(self, prog):
        instr_iter = iter(prog)
        xlist = []
        try:
            while True:
                #print(self)
                xlist.append(self.x)
                self.cycle(instr_iter)
        except StopIteration:
            return xlist

    def cycle(self, instr_iter):
        if self.state == State.Fetch:
            field = next(instr_iter).split()
            #print('\tfetched', field)
            if field[0] == 'noop':
                return
            elif field[0] == 'addx':
                self.v = int(field[1])
                self.state = State.Adding
                return
            else:
                raise ValueError('operation', field[0])
        elif self.state == State.Adding:
            self.x += self.v
            self.state = State.Fetch
            return
        else:
            raise ValueError('state', self.state)


def part1(prog):
    cpu = CPU()
    output = cpu.run(prog)
    signalsum = 0
    for cyclenum, x in enumerate(output, start=1):
        if cyclenum in [20, 60, 100, 140, 180, 220]:
            signal = cyclenum * x
            signalsum += signal
    return signalsum


def part2(prog):
    cpu = CPU()
    output = cpu.run(prog)
    crt = []
    for crtpos, x in enumerate(output):
        if abs((crtpos % 40) - x) <= 1:
            crt.append('*')
        else:
            crt.append(' ')
        #print(f'crtpos {crtpos:02d} sprite {list(range(x-1, x+2))} \terr {abs((crtpos % 40) - x):02d} crt {"".join(crt)}')

    for rowstart in range(0, len(crt), 40):
        row = crt[rowstart: rowstart + 40]
        print(''.join(row))


def checkexamples():
    with open('example.txt') as prog:
        example1 = part1(prog)
        print('example1', example1)
        assert example1 == 13140

    with open('example.txt') as prog:
        print('example2')
        part2(prog)


def main():
    checkexamples()
    with open('input.txt') as prog:
        print('part1', part1(prog))
    
    with open('input.txt') as prog:
        print('part2')
        part2(prog)

if __name__ == '__main__':
    main()