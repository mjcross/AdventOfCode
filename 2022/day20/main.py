from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy

class Buffer:
    _items: list

    def __init__(self, items):
        self._items = items
        self.modulus = len(items) - 1
        self.maxshift = (len(items) - 1) // 2
        for self.zero in items:
            if self.zero.value == 0:
                break
        else:
            raise ValueError('no zero item')

    def __repr__(self):
        """ Full representation including links """
        repr = ''
        item = self.zero
        while True:
            repr += f'{item}\n'
            item = item.right
            if item == self.zero:
                return repr

    def __str__(self):
        """ Abbreviated representation with just values """
        repr = ''
        item = self.zero
        while True:
            repr += f'{item.value:4} '
            item = item.right
            if item == self.zero:
                return repr

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def walk_left(self, item, shift):
        shift = shift % -len(self)
        if shift:
            if shift < -len(self) // 2:
                # quicker to go the other way
                return self.walk_right(item, shift + len(self))
            else:
                # walk left
                while shift:
                    item = item.left
                    shift += 1            
        return item

    def walk_right(self, item, shift):
        shift = shift % len(self)
        if shift:
            if shift > len(self) // 2:
                # quicker to go the other way
                return self.walk_left(item, shift - len(self))
            else:
                # walk right
                while shift:
                    item = item.right
                    shift -= 1
        return item

    def move_left(self, item, shift):
        shift = shift % -self.modulus
        if shift:
            if shift < -self.modulus:
                # quicker to go the other way
                self.move_right(item, shift + self.modulus)
            else:
                # find insert position
                insert_pos = item
                while shift:
                    insert_pos = insert_pos.left
                    shift += 1

                # unlink from current position
                item.left.right = item.right
                item.right.left = item.left

                # relink to left of new position
                item.right = insert_pos
                item.left = insert_pos.left
                insert_pos.left.right = item
                insert_pos.left = item

    def move_right(self, item, shift):
        shift = shift % self.modulus
        if shift:
            if shift > self.maxshift:
                # quicker to go the other way
                self.move_left(item, shift - self.modulus)
            else:
                # find insert position
                insert_pos = item

                while shift:
                    insert_pos = insert_pos.right
                    shift -= 1

                # unlink from current position
                item.left.right = item.right
                item.right.left = item.left

                # relink to right of new position
                item.left = insert_pos
                item.right = insert_pos.right
                insert_pos.right.left = item
                insert_pos.right = item

    def move(self, item, shift):
        if shift > 0:
            self.move_right(item, shift)
        elif shift < 0:
            self.move_left(item, shift)
            

@dataclass
class Item:
    value: int
    left: Item
    right: Item

    def __repr__(self):
        return f'{self.left.value if self.left else "None":^5} <<< {self.value:^5d} >>> {self.right.value if self.right else "None":^5}'

    def __str__(self):
        return f'{self.value}'


def parse(stream):
    items = [Item(int(line), None, None) for line in stream]
    prev_item = items[-1]
    item_iter = iter(items)
    while True:
        try:
            this_item = next(item_iter)
            prev_item.right = this_item
            this_item.left = prev_item
            prev_item = this_item
        except StopIteration:
            break
    
    return Buffer(items)


def mix(buffer):
    for item in buffer:
        buffer.move(item, item.value)


def score(buffer):
    score = 0
    item = buffer.zero
    for _ in range(3):
        item = buffer.walk_right(item, 1000)
        score += item.value
    return score


def part1(stream):
    buffer = parse(stream)
    mix(buffer)
    return score(buffer)


def part2(stream):
    buffer = parse(stream)
    for item in buffer:
        item.value *= 811589153
    print('\tmixing:', end=' ')
    for step in range(10):
        print(f'{step + 1}', end=' ')
        mix(buffer)
    print()
    return score(buffer)



def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 3

    with open('example.txt') as stream:
        result = part2(stream)
        print(f'example2: {result}')
        assert result == 1623178306


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print(f'part1: {result}')

    with open('input.txt') as stream:
        result = part2(stream)
        print(f'part2: {result}')


if __name__ == '__main__':
    main()