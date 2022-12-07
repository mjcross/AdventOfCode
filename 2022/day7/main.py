class Dirnode:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.filetot = 0
        self.files = {}
        self.dirs = {}

    def __repr__(self):
        #return f'\nDirnode(name={self.name}, filetot={self.filetot}, files={self.files.items()}, dirs={self.dirs}'
        return f'(Dirnode({self.name})'

    def adddir(self, dirname):
        self.dirs[dirname] = Dirnode(name=dirname, parent=self)

    def addfile(self, name, size):
        self.files[name] = size
        self.filetot += size

    def dirsize(self):
        return self.filetot + sum([dir.dirsize() for dir in self.dirs.values()])

    def dirlist(self):
        li = [self]
        for subdir in self.dirs.values():
            li += subdir.dirlist()
        return li


def maketree(lines):
    root = Dirnode('/', parent=None)
    node = root
    for line in lines:
        field = line.split()
        if field[0] == '$':
            if field[1] == 'cd':
                if field[2] == '/':
                    node = root
                elif field[2] == '..':
                    assert node.parent
                    node = node.parent
                else:
                    node = node.dirs[field[2]]
            elif field[1] == 'ls':
                pass
            else:
                raise ValueError(line)
        elif field[0] == 'dir':
            node.adddir(field[1])
        else:
            node.addfile(name=field[1], size=int(field[0]))
    return root

def part1(tree):
    smalldirs = 0
    for dir in tree.dirlist():
        size = dir.dirsize()
        if size <= 100000:
            smalldirs += size

    return smalldirs

def part2(tree):
    dirsize = sorted([dir.dirsize() for dir in tree.dirlist()])
    disksize = 70000000
    free = disksize - dirsize[-1]
    updatesize = 30000000
    for size in dirsize:
        if size + free >= updatesize:
            return size


def checkexamples():
    lines = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".split('\n')

    answer = 95437, 24933642
    tree = maketree(lines)
    
    assert part1(tree) == answer[0]
    assert part2(tree) == answer[1]


def main():
    checkexamples()
    with open('input.txt') as infile:
        tree = maketree(infile.readlines())
        print(part1(tree))
        print(part2(tree))

if __name__ == '__main__':
    main()