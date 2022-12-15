def iterate2d(x1, y1, x2, y2):
    dx = min(1, max(-1, x2 - x1))
    dy = min(1, max(-1, y2 - y1))
    x, y = x1, y1
    yield x, y
    while x != x2 or y!= y2:
        if x != x2:
            x += dx
        if y != y2:
            y += dy
        yield x, y


def main():
    for x,y in iterate2d(4, 3, 6, 10):
        print(x, y)

if __name__ == '__main__':
    main()