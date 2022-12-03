import math

def sign(x):
    if x >= 0:
        return 1.0
    elif x < 0:
        return -1.0
class Point2d:
    def __init__(self, x, y = None):
        if type(x) is tuple:
            self.x = x[0]
            self.y = x[1]
        elif type(x) is Point2d:
            self.x = x.x
            self.y = x.y
        else:
            self.x = x
            self.y = y or 0.0

    def floated(self):
        return Point2d(float(self.x), float(self.y))
    def inted(self):
        return Point2d(int(self.x), int(self.y))

    def floats(self):
        return float(self.x), float(self.y)
    def ints(self):
        return int(self.x), int(self.y)

    def transpose(self):
        return self.y, self.x
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

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

    def __repr__(self):
        return f"(x = {self.x}, y = {self.y})"

    def ang(self, other): # rotation of other to get self and other aligned
        lnorm = self.norm()
        rnorm = other.norm()
        if lnorm > 1e-05 and rnorm > 1e-05:
            lnormed = self / lnorm
            rnormed = other / rnorm
            return lnormed.angNormed(rnormed)
        else:
            return None

    def cos_sin(self, other):
        lnorm = self.norm()
        rnorm = other.norm()
        if lnorm > 1e-05 and rnorm > 1e-05:
            lnormed = self / lnorm
            rnormed = other / rnorm
            return lnormed.cos_cin_normed(rnormed)
        else:
            return None, None

    def angNormed(self, other):
        cosine, sine = self.cos_sin_normed(other)
        angle = math.acos(cosine)
        return sign(sine) * angle

    def cos_sin_normed(self, other):
        cosine = self.dot(other)
        sine = self.cross(other)
        return cosine, sine

    def rotateByCosSin(self, cosine, sine):
        return Point2d(self.x*cosine - self.y*sine, self.y*cosine + self.x*sine)

    
    def distToSegment(self, a, b):
        da = a - self
        dan = da.norm()
        db = b - self
        dbn = db.norm()
        t = a - b
        tn = t.norm()
        if tn < 1e-05:
            return 0.5 * (dan + dbn)
        t = t / tn
        n = t.rotateByCosSin(0.0, 1.0)
        dlp = n.dot(da)
        p = self + n * dlp
        if (a-p).dot(b-p) < 0:
            return abs(dlp)
        else:
            return min(dan, dbn)



