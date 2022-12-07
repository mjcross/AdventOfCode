class Node:
    def __init__(self, path=''):
        self.weight = [0, 0]
        self.node = [None, None]
        self.path = path

    def isleaf(self):
        return self.weight == [0, 0]

    def add(self, bit):
        if self.node[bit] is None:
            self.node[bit] = Node(path=self.path + str(bit))
        self.weight[bit] += 1
        return self.node[bit]

    def __repr__(self):
        return f'Node(path={self.path}, weight={self.weight})'


def maketree(words):
    root = Node()
    for word in words:
        node = root
        for bit in word.rstrip():
            node = node.add(int(bit))
    return root


def part1(words):
    words = [word.rstrip() for word in words]
    gammastr = ''
    epsilonstr = ''
    wordlen = len(words[0])
    for index in range(wordlen):
        count = [0, 0]
        for word in words:
            bit = int(word[index])
            count[bit] += 1
        if count[1] > count[0]:
            gammastr += '1'
            epsilonstr += '0'
        else:
            gammastr += '0'
            epsilonstr += '1'
    return int(gammastr, 2) * int(epsilonstr, 2)
 

def part2(root):
    node = root
    while not node.isleaf():
        if node.weight[0] > node.weight[1]:
            node = node.node[0]
        else:
            node = node.node[1]
    oxygen = int(node.path, 2)
    node = root
    while not node.isleaf():
        if node.weight[0] == 0:
            node = node.node[1]
        elif node.weight[1] == 0:
            node = node.node[0]
        elif node.weight[0] <= node.weight[1]:
            node = node.node[0]
        else:
            node = node.node[1] 
    co2 = int(node.path, 2)
    return oxygen * co2


def checkexamples():
    example = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
    answer = 198, 230
    words = example.split('\n')
    print('example 1', part1(words) == answer[0])
    tree = maketree(words)
    print('example 2', part2(tree) == answer[1])


def main():
    checkexamples()

    with open('input.txt') as infile:
        words = [line.strip() for line in infile]
        print(part1(words))
        tree = maketree(words)
        print(part2(tree))

if __name__ == '__main__':
    main()