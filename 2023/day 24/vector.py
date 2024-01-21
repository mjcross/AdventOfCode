from dataclasses import dataclass
from typing import Self
from math import hypot

@dataclass
class Point:
    x: int
    y: int
    z: int

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z})'

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __iadd__(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __isub__(self, other: Self) -> Self:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    
    def __iter__(self):
        """so we can (e.g.) make a numpy array from the point"""
        for ordinate in [self.x, self.y, self.z]:
            yield ordinate


@dataclass
class Vector(Point):

    def __mul__(self, k: int) -> Self:
        return Vector(k * self.x, k * self.y, k * self.z)

    __rmul__ = __mul__

    def __neg__(self) -> Self:
        return Vector(-self.x, -self.y, -self.z)

    def __truediv__(self, d: int) -> Self:
        return Vector(self.x / d, self.y / d, self.z / d)

    @property
    def magnitude(self):
        return hypot(self.x, self.y, self.z)

    @property
    def unitvector(self):
        return self / self.magnitude

    
    def dot(self, other: Self) -> int:        
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(a: Self, b: Self) -> Self:
        """formula from https://www.statology.org/cross-product-python/"""
        return Vector(
            a.y * b.z - a.z * b.y,
            a.z * b.x - a.x * b.z,
            a.x * b.y - a.y * b.x
        )
    
    def isparallel(a: Self, b: Self) -> bool:
        return a.cross(b) == Vector(0, 0, 0)


def main():
    """some simple tests"""
    normal = (0, 0, 1)
    x1 = Vector(1, 0, 0)
    y1 = Vector(0, 1, 0)
    z1 = Vector(0, 0, 1)

    assert z1.cross(y1) == -x1
    assert z1.cross(x1) == y1

    print(y1.cross(z1), z1.cross(x1))

    print(Vector.zero())


if __name__ == '__main__':
    main()