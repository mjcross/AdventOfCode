from collections import deque

dq = deque(range(10))
print(dq)
dq.extendleft(list('abc'))
print(dq)
v = dq.popleft(2)
print (v, dq)