import math

class Point2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def floats(self):
        return float(self.x), float(self.y)
    def ints(self):
        return int(self.x), int(self.y)

    def transpose(self):
        return self.y, self.x
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __tuple__(self):
        return self.x, self.y

    def __add__(self, other):
        return Point2d(self.x + other.x, self.y + other.y)

    # def __iadd__(self, other):
    #     self = self + other

    def __sub__(self, other):
        return Point2d(self.x - other.x, self.y - other.y)

    # def __isub__(self, other):
    #     self = self - other

    def __mul__(self, scalar):
        return Point2d(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Point2d(self.x / scalar, self.y / scalar)

    def norm(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalize(self):
        return self / self.norm()

    def renormalize(self, new_norm=1.0):
        return self.normalize() * new_norm

