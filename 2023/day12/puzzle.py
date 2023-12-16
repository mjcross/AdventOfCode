from dataclasses import dataclass

def binstr(bits:int, nbits:int):
    return f'{bits:0{nbits}b}'

nbits = [2**n - 1 for n in range(25)]

@dataclass
class Puzzle:
    length: int
    setbits: int
    clrbits: int
    groups: list[int]
    text: str

    def __str__(self):
        return 'Puzzle: '+ (' ').join([
            self.text + '\t',
            'set: ' + binstr(self.setbits, self.length),
            'clr: ' + binstr(self.clrbits, self.length),
            str(self.groups)
        ])
    

def iterateDebug(p: Puzzle, prevX: int, start: int, depth: int = 0):
    indentStr = '\t' * depth
    sz = p.groups.pop()

    # space for remaining groups
    otherSz = sum(p.groups) + len(p.groups) - 1     # no padding for last group
    bits = nbits[sz]

    nValid = 0
    for shift in range(start, p.length - (sz + otherSz)):
        mask = nbits[shift + sz + 1]    # allow extra bit for padding
        x = prevX | (bits << shift)

        print(indentStr, 'x:    ', binstr(x, p.length))
        print(indentStr, 'mask: ', binstr(mask, p.length))

        # check validity
        if x & p.clrbits == 0 and (x ^ mask) & p.setbits == 0:
            print(indentStr, 'valid')
            if len(p.groups) == 0:
                print(indentStr, 'all placed', nValid)

                # all groups placed - check high order setbits
                if (x ^ nbits[p.length]) & p.setbits == 0:
                    nValid += 1

                    #! extended validation
                    for combo, spec in zip(binstr(x, p.length), p.text):
                        if spec == '.' and combo != '0':
                            print(p)
                            print('       ', binstr(x, p.length))
                            print('fails clrbit')
                            raise ValueError
                        if spec == '#' and combo != '1':
                            print(p)
                            print('       ', binstr(x, p.length))
                            print('fails setbit')
                            raise ValueError

                else:
                    print(indentStr, 'high order set clear')

            else:
                nValid += iterateDebug(
                    Puzzle(p.length, p.setbits, p.clrbits, p.groups.copy(), p.text), 
                    x, shift + sz + 1, depth + 1)
        else:
            if x & p.clrbits:
                print(indentStr, 'clr set')
            if (x ^ mask) & p.setbits:
                print(indentStr, 'set clear')

    print(indentStr, 'total:', nValid)         
    return nValid


def iterate(p: Puzzle, prevX: int, start: int):
    sz = p.groups.pop()

    # space for remaining groups
    otherSz = sum(p.groups) + len(p.groups) - 1     # no padding for last group
    bits = nbits[sz]

    nValid = 0
    for shift in range(start, p.length - (sz + otherSz)):
        mask = nbits[shift + sz + 1]    # allow extra bit for padding
        x = prevX | (bits << shift)

        # check validity
        if x & p.clrbits == 0 and (x ^ mask) & p.setbits == 0:
            if len(p.groups) == 0:
                # all groups placed - check high order setbits
                if (x ^ nbits[p.length]) & p.setbits == 0:
                    nValid += 1

            else:
                nValid += iterate(
                    Puzzle(p.length, p.setbits, p.clrbits, p.groups.copy(), p.text), 
                    x, shift + sz + 1)

    return nValid