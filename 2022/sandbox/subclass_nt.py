from typing import NamedTuple, Any
from dataclasses import dataclass

ORE = 1
CLAY = 2

class FooTuple(NamedTuple):
    item1: Any
    item2: Any

    def __hash__(self):
        return hash(self.item1) * hash(self.item2)

@dataclass
class FooClass:
    item1: Any
    item2: Any

    def __hash__(self):
        return hash(self.item1) * hash(self.item2)



def main():
    ft = FooTuple(2,3)
    print(ft, ft.item2)

    fc = FooClass(2,3)
    print(fc, fc.item2)

    for mat in (ORE, CLAY):
        print(mat)

if __name__ == '__main__':
    main()