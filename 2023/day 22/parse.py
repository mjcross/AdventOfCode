from dataclasses import dataclass

@dataclass
class Point3D:
    x: int
    y: int
    z: int

    def __str__(self):
        return f'{self.x},{self.y},{self.z}'
    
    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
    

class Brick:
    index: int
    min: Point3D
    max: Point3D
    supportsIndices: set

    def __init__(self, index, t1, t2):
        self.index = index
        self.min = Point3D(*t1)
        self.max = Point3D(*t2)
        if self.min.x > self.max.x or self.min.y > self.min.y or self.min.z > self.max.z:
            self.min, self.max = self.max, self.min
        self.supportsIndices = set()

    def __str__(self):
        return f'Brick {self.index}: {self.min} ~ {self.max}'

    def __gt__(self, other):
        return self.min.z > other.min.z
    
    def __lt__(self, other):
        return self.max.z < other.max.z
    
    def getTopBottom(self):
        top = []
        bottom = []
        for x in range(self.min.x, self.max.x + 1):
            for y in range(self.min.y, self.max.y +1 ):
                top.append(Point3D(x, y, self.max.z))
                bottom.append(Point3D(x, y, self.min.z))
        return top, bottom


def parse(stream) -> list[Brick]:
    bricks = []
    for index, rawline in enumerate(stream):
        line = rawline.strip()
        point1Str, point2Str = line.split('~')
        x1, y1, z1 = map(int, point1Str.split(','))
        x2, y2, z2 = map(int, point2Str.split(','))
        bricks.append(Brick(index, (x1, y1, z1), (x2, y2, z2)))
    return bricks