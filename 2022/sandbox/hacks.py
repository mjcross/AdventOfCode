seq = (199, 200, 208, 210, 200, 207, 240, 269, 260, 263)

class mylist(list):
    
    def delta(self):
        previtem = self[0]
        for thisitem in self[1:]:
            yield thisitem - previtem
            previtem = thisitem


    def windowed(self, size):
        i = 0
        while i + size <= len(seq):
            yield(self[i: i + size])
            i += 1

li = mylist(range(10))
print(li, list(li.delta()), list(li.windowed(4)))