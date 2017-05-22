import numpy as np

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.norm = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)

    def to_string(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def relative_direction(v1, v2=Vector(1, 0, 0)):
    return np.arccos(dot(v1, v2) / (v1.norm * v2.norm))


def color_map(angle):
    return np.ceil(np.array(angle * 255) / np.pi)


def rescale(value, max_val, max_rescaled):
    return (value * max_rescaled) / max_val
