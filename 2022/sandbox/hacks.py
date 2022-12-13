class MyClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return(f'{self.value}')

    def __lt__(self, other):
        print('lt')
        return self.value > other.value


seq = [MyClass(x) for x in [5,2,4,2,3]]
print(sorted(seq, reverse=True))