from random import randint

class MyClass:
    def __init__(self, index, a, b, c):
        self.index = index
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return f'MyClass(index={self.index}, a={self.a}, b={self.b}, c={self.c})'


def dedupe(items):
    itemdict = {}
    for item in items:
        itemdict[(item.a, item.b, item.c)] = item.index
    return itemdict


def main():
    items = []
    for index in range(1000):
        items.append(MyClass(index=index, a=randint(1, 5), b=randint(1,5), c=randint(1,5)))

    nodupes = dedupe(items)

    print(len(nodupes))

    

if __name__ == '__main__':
    main()