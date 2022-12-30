from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy

class Buffer:
    _items: list
    head: Item

    def __init__(self, items):
        self._items = items
        self.head = items[0]

    def __repr__(self):
        repr = ''
        item = self.head
        while True:
            repr += f'{item}\n'
            item = item.right
            if item == self.head:
                return repr

    def __str__(self):
        repr = ''
        item = self.head
        while True:
            repr += f'{item.value:4} '
            item = item.right
            if item == self.head:
                return repr

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def pos(self, value):
        pos = 0
        item = self.head
        while True:
            if item.value == value:
                return pos
            else:
                pos += 1
                item = item.right
        else:
            raise ValueError

    def reduced_shift(self, shift):
        if shift % len(self) == 0:
            return 0
        elif shift < 0:
            alt_shift = (shift - 1) % len(self)
        elif shift > 0:
            alt_shift = (shift + 1) % -len(self)

        if abs(alt_shift) < abs(shift):
            # quicker to go the other way
            return alt_shift
        else:
            return shift

    def move(self, item, shift):
        # minimise number of steps
        reduced_shift = self.reduced_shift(shift)
        if reduced_shift:
            # unlink at current position
            item.left.right = item.right
            item.right.left = item.left

            if reduced_shift > 0:
                #* >>>> MOVE ITEM RIGHT >>>>
                new_pos = item
                while reduced_shift > 0:
                    # walk right
                    new_pos = new_pos.right
                    reduced_shift -= 1
                # insert to the right of new_pos
                if item == self.head:
                    # moving the head to the right always creates a new head
                    self.head = item.right
                item.left = new_pos
                item.right = new_pos.right
                new_pos.right.left = item
                new_pos.right = item

            elif reduced_shift < 0:
                #* <<<< MOVE ITEM LEFT <<<<
                new_pos = item
                while reduced_shift < 0:
                    # walk left
                    new_pos = new_pos.left
                    reduced_shift += 1
                # insert to the left of new_pos
                if item == self.head:
                    # moving the head to the left creates a new head
                    self.head = item.right
                #elif new_pos == self.head:
                    # inserting to the left of head makes a new head
                #    self.head = item
                item.right = new_pos
                item.left = new_pos.left
                new_pos.left.right = item
                new_pos.left = item


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


def part1(stream):
    buffer = parse(stream)
    #print('Initial arrangement:')
    #print(buffer)
    #print()
    for index in range(len(buffer)):
        item = buffer[index]
        buffer.move(item, item.value)
        #print(f'{item} moves between {item.left} and {item.right}: ')
        #print(buffer)
        #print()
    
    # find the zero
    for item in buffer._items:
        if item.value == 0:
            break
    else:
        raise ValueError
    
    score = 0
    pos_shift = 1000 % len(buffer)  #! might be quicker to shift the other way
    for _ in range(3):
        shift = pos_shift
        if shift > 0:
            while shift:
                item = item.right
                shift -= 1
        elif shift < 0:
            while shift:
                item = item.left
                shift += 1
        score += item.value
        print(item)
    return score


def part2(stream):
    pass


def checkexamples():
    with open('example.txt') as stream:
        result = part1(stream)
        print(f'example1: {result}')
        assert result == 3

    #with open('example.txt') as stream:
    #    result = part2(stream)
    #    assert result == 'xxxxx', result


def main():
    checkexamples()

    with open('input.txt') as stream:
        result = part1(stream)
        print('part1', result)

    #with open('input.txt') as stream:
    #    print('part2', part2(stream))


if __name__ == '__main__':
    main()