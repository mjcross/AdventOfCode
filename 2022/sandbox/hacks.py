from itertools import cycle

x = [1,2,3]

it = cycle(x)

for _ in range(10):
    print(next(it))

l = [next(it)] * 7
print(l)