from utils.array2d import Array2D
from enum import Enum
from collections import namedtuple

FREE = ord('.')
WALL = ord('#')
EDGE = ord(' ')

DirectionTuple = namedtuple('DirectionTuple', 'symbol dx dy score')
LinkTuple = namedtuple('LinkTuple', 'dest facing')
Point = namedtuple('Point', 'x y')


class Direction(Enum):
    RIGHT = DirectionTuple(ord('>'), 1, 0, 0)
    DOWN = DirectionTuple(ord('v'), 0, 1, 1)
    LEFT = DirectionTuple(ord('<'), -1, 0, 2)
    UP = DirectionTuple(ord('^'), 0, -1, 3)

    def __repr__(self):
        return self.name


turn_right = {
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
    Direction.UP: Direction.RIGHT
}

turn_left = {
    Direction.RIGHT: Direction.UP,
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT
}


class Board:
    def __init__(self, grid, facing=Direction.RIGHT, edge_map={}):
        self.grid = grid
        self.facing = facing
        self.edge_map = edge_map
        self.find_start()

    def __repr__(self):
        return self.grid.as_chars()

    def find_start(self):
        self.y = 0
        self.x = 0
        while self.grid[self.x, self.y] != FREE:
            self.x += 1
        self.grid[self.x, self.y] = self.facing.value.symbol

    def turn_right(self):
        self.facing = turn_right[self.facing]
        self.grid[self.x, self.y] = self.facing.value.symbol

    def turn_left(self):
        self.facing = turn_left[self.facing]
        self.grid[self.x, self.y] = self.facing.value.symbol

    def lookahead(self):
        x = self.x + self.facing.value.dx
        y = self.y + self.facing.value.dy
        if self.grid[x, y] == EDGE:
            if self.edge_map:
                # move to adjacent edge of cube
                (x, y), facing = self.edge_map[Point(self.x, self.y), self.facing]
                return self.grid[x, y], x, y, facing
            else:
                # move backwards until about to move off the opposite edge
                while self.grid[x - self.facing.value.dx, y - self.facing.value.dy] != EDGE:
                    x -= self.facing.value.dx
                    y -= self.facing.value.dy
        return self.grid[x, y], x, y, self.facing

    def advance(self, spaces):
        while spaces:
            block_ahead, next_x, next_y, next_facing = self.lookahead()
            if block_ahead == WALL:
                break
            else:
                self.x = next_x
                self.y = next_y
                self.facing = next_facing
                self.grid[self.x, self.y] = self.facing.value.symbol
            spaces -= 1

    def do_command(self, command):
        if type(command) is int:
            self.advance(command)
        elif command is Direction.RIGHT:
            self.turn_right()
        elif command is Direction.LEFT:
            self.turn_left()
        else:
            raise ValueError(f'unrecognised command: {command}')

    def do_route(self, command_list):
        for command in command_list:
            self.do_command(command)

    def get_password(self):
        return 1000 * (self.y + 1) + 4 * (self.x + 1) + self.facing.value.score


def parse(stream):
    lines = stream.readlines()
    height = 0
    width = 0
    line = lines[0]

    map_lines = []
    line_iter = iter(lines)
    line = next(line_iter).rstrip()
    while line:
        width = max(height, len(line))
        height += 1
        map_lines.append(line)
        line = next(line_iter).rstrip()

    command_str = next(line_iter)
    
    grid = Array2D('B', xmin=-1, xmax=width, ymin=-1, ymax=height, initialvalue=EDGE)
    for y, line in enumerate(map_lines):
        for x, character in enumerate(line.rstrip()):
            grid[x, y] = ord(character)

    return grid, command_str


def make_edge_links(size, folding=1):
    Face = namedtuple('Face', 'top right bottom left')
    faces = [None]  # dummy face 0

    # face top-left corners
    if folding == 1:
        origins = [
            Point(2 * size, 0),         # face 1
            Point(0, 1 * size),         # face 2
            Point(1 * size, 1 * size),  # face 3
            Point(2 * size, 1 * size),  # face 4
            Point(2 * size, 2 * size),  # face 5
            Point(3 * size, 2 * size)   # face 6
        ]
    elif folding == 2:
        origins = [
            Point(1 * size, 0),         # face 1
            Point(2 * size, 0),         # face 2
            Point(1 * size, 1 * size),  # face 3
            Point(0, 2 * size),         # face 4
            Point(1 * size, 2 * size),  # face 5
            Point(0, 3 * size)          # face 6
        ]
    else: raise ValueError(f'unrecognised folding: {folding}')

    # face edge elements
    for origin in origins:
        top = [Point(origin.x + i, origin.y) for i in range(size)]
        right = [Point(origin.x + size - 1, origin.y + i) for i in range(size)]
        bottom = [Point(origin.x + i, origin.y + size - 1) for i in range(size)]
        left = [Point(origin.x, origin.y + i) for i in range(size)]
        faces.append(Face(top, right, bottom, left))

    # link to adjacent face elements
    links = {}

    if folding == 1:    # folding as per example
        # face 1
        for src, dest in zip(faces[1].top, reversed(faces[2].top)):
            links[(src, Direction.UP)] = LinkTuple(dest, Direction.DOWN)
        for src, dest in zip(faces[1].right, reversed(faces[6].right)):
            links[(src, Direction.RIGHT)] = LinkTuple(dest, Direction.LEFT)
        for src, dest in zip(faces[1].left, faces[3].top):
            links[(src, Direction.LEFT)] = LinkTuple(dest, Direction.DOWN)

        # face 2
        for src, dest in zip(faces[2].top, reversed(faces[1].top)):
            links[(src, Direction.UP)] = LinkTuple(dest, Direction.DOWN)
        for src, dest in zip(faces[2].bottom, reversed(faces[5].bottom)):
            links[(src, Direction.DOWN)] = LinkTuple(dest, Direction.UP)
        for src, dest in zip(faces[2].left, reversed(faces[6].bottom)):
            links[(src, Direction.LEFT)] = LinkTuple(dest, Direction.UP)

        # face 3
        for src, dest in zip(faces[3].top, faces[1].left):
            links[(src, Direction.UP)] = LinkTuple(dest, Direction.RIGHT)
        for src, dest in zip(faces[3].bottom, reversed(faces[5].left)):
            links[(src, Direction.DOWN)] = LinkTuple(dest, Direction.RIGHT)

        # face 4
        for src, dest in zip(faces[4].right, reversed(faces[6].top)):
            links[(src, Direction.RIGHT)] = LinkTuple(dest, Direction.DOWN)
        
        # face 5
        for src, dest in zip(faces[5].bottom, reversed(faces[2].bottom)):
            links[(src, Direction.DOWN)] = LinkTuple(dest, Direction.UP)
        for src, dest in zip(faces[5].left, reversed(faces[3].bottom)):
            links[(src, Direction.LEFT)] = LinkTuple(dest, Direction.UP)

        # face 6
        for src, dest in zip(faces[6].top, reversed(faces[4].right)):
            links[(src, Direction.UP)] = LinkTuple(dest, Direction.LEFT)
        for src, dest in zip(faces[6].right, reversed(faces[1].right)):
            links[(src, Direction.RIGHT)] = LinkTuple(dest, Direction.LEFT)
        for src, dest in zip(faces[6].bottom, reversed(faces[2].left)):
            links[(src, Direction.DOWN)] = LinkTuple(dest, Direction.RIGHT)

    elif folding ==2:   # folding as per puzzle
        # face 1
        for src, dest in zip(faces[1].top, faces[6].left):
            links[(src, Direction.UP)] = LinkTuple(dest, Direction.RIGHT)
        for src, dest in zip(faces[1].left, reversed(faces[4].left)):
            links[(src, Direction.LEFT)] = LinkTuple(dest, Direction.RIGHT)

        # face 2
        for src, dest in zip(faces[2].top, faces[6].bottom):
            links[(src, Direction.UP)] = LinkTuple(dest, Direction.UP)
        for src, dest in zip(faces[2].right, reversed(faces[5].right)):
            links[(src, Direction.RIGHT)] = LinkTuple(dest, Direction.LEFT)
        for src, dest in zip(faces[2].bottom, faces[3].right):
            links[(src, Direction.DOWN)] = LinkTuple(dest, Direction.LEFT)

        # face 3
        for src, dest in zip(faces[3].right, faces[2].bottom):
            links[(src, Direction.RIGHT)] = LinkTuple(dest, Direction.UP)
        for src, dest in zip(faces[3].left, faces[4].top):
            links[(src, Direction.LEFT)] = LinkTuple(dest, Direction.DOWN)

        # face 4
        for src, dest in zip(faces[4].top, faces[3].left):
            links[(src, Direction.UP)] = LinkTuple(dest, Direction.RIGHT)
        for src, dest in zip(faces[4].left, reversed(faces[1].left)):
            links[(src, Direction.LEFT)] = LinkTuple(dest, Direction.RIGHT)

        # face 5
        for src, dest in zip(faces[5].right, reversed(faces[2].right)):
            links[(src, Direction.RIGHT)] = LinkTuple(dest, Direction.LEFT)
        for src, dest in zip(faces[5].bottom, faces[6].right):
            links[(src, Direction.DOWN)] = LinkTuple(dest, Direction.LEFT)

        # face 6
        for src, dest in zip(faces[6].right, faces[5].bottom):
            links[(src, Direction.RIGHT)] = LinkTuple(dest, Direction.UP)
        for src, dest in zip(faces[6].bottom, faces[2].top):
            links[(src, Direction.DOWN)] = LinkTuple(dest, Direction.DOWN)
        for src, dest in zip(faces[6].left, faces[1].top):
            links[(src, Direction.LEFT)] = LinkTuple(dest, Direction.DOWN)

    else: raise ValueError(f'unrecognised folding: {folding}')

    return links


def parse_commands(command_str):
    command_list = list(command_str)
    commands = []
    num = ''
    while command_list:
        c = command_list.pop(0)
        if c == 'R':
            if num:
                commands.append(int(num))
                num = ''
            commands.append(Direction.RIGHT)
        elif c == 'L':
            if num:
                commands.append(int(num))
                num = ''
            commands.append(Direction.LEFT)
            num = ''
        else:
            num += c
    if num:
        commands.append(int(num))
    return commands


def part1(stream):
    grid, command_str = parse(stream)
    board = Board(grid)
    route = parse_commands(command_str)
    board.do_route(route)
    print(board)
    return board.get_password()


def part2(stream, face_size, folding):
    grid, command_str = parse(stream)
    edge_links = make_edge_links(size=face_size, folding=folding)
    board = Board(grid, edge_map=edge_links)
    route = parse_commands(command_str)
    board.do_route(route)
    print(board)
    return board.get_password()


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 6032

    with open('example.txt') as stream:
        result = part2(stream, face_size=4, folding=1)
        print(f'example2: {result}')
        assert result == 5031, result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1 {result}')

    with open('input.txt') as stream:
        result = part2(stream, face_size=50, folding=2)
        print(f'part2 {result}')


if __name__ == '__main__':
    main()