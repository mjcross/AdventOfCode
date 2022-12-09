from array import array

def func(x):
    x[4] = 99

a = array('B', range(20))
func(a[5: None: 3])

print(a)