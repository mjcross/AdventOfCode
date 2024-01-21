from dataclasses import dataclass
from vector import Vector

@dataclass
class Body:
    p0: Vector
    v: Vector

    def at_time(self, t:int) -> Vector:
        return self.p0 + self.v * t
    
    def __sub__(self, other):
        return Body(self.p0 - other.p0, self.v - other.v)
    
    def __iadd__(self, other):
        self.p0 += other.p0
        self.v += other.v
        return self


def parse(stream):
    stones = []
    for rawline in stream:
        line = rawline.strip()

        pStr, vStr = line.split('@')

        p = map(int, pStr.split(','))
        v = map(int, vStr.split(','))

        stones.append(Body(Vector(*p), Vector(*v)))

    return stones
