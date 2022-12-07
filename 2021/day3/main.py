import pprint
pp = pprint.PrettyPrinter(indent=4)

def maketree(wordlist):
    tree = [[],[]]
    for word in wordlist:
        for bitchar in word:
            tree[int(bitchar)] = [[],[]]
    pp.pprint(tree)


def majority(wordlist):
    bitcounts = [0] * len(wordlist[0])
    for word in wordlist:
        for index, bit in enumerate(word):
            if bit == '1':
                bitcounts[index] += 1
    threshold = len(wordlist) // 2
    maketree(wordlist)
    return [int(count >= threshold) for count in bitcounts]


def part1(wordlist):
    gammastr = ''
    epsilonstr = ''
    for bit in majority(wordlist):
        if bit:
            gammastr += '1'
            epsilonstr += '0'
        else:
            gammastr += '0'
            epsilonstr += '1'
    return int(gammastr, base=2) * int(epsilonstr, base=2)


def part2(wordlist):
    while len(wordlist) > 1:
        pass


def checkexamples():
    examples = [
        (
            ('00100',
            '11110',
            '10110',
            '10111',
            '10101',
            '01111',
            '00111',
            '11100',
            '10000',
            '11001',
            '00010',
            '01010'), (198,)
        )
    ]
    for data, answer in examples:
        assert part1(data) == answer[0]
        #assert part2(data) == answer[1]


def main():
    checkexamples()

    with open('input.txt') as infile:
        datalist = [line.strip() for line in infile]
        print(part1(datalist))
        #print(part2())

if __name__ == '__main__':
    main()