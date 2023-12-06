def iterate2d(x_start, y_start, x_end, y_end):
    dx = min(1, max(-1, x_end - x_start))
    dy = min(1, max(-1, y_end - y_start))
    x, y = x_start, y_start
    yield x, y
    while x != x_end or y!= y_end:
        if x != x_end:
            x += dx
        if y != y_end:
            y += dy
        yield x, y


def main():
    for x,y in iterate2d(4, 3, 6, 10):
        print(x, y)

if __name__ == '__main__':
    main()