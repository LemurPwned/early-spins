import numpy as np
import pandas as pd

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.norm = np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)


def dot(v1,v2):
        return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z

def relative_direction(v1, v2=Vector(1,0,0)):
        return np.arccos(dot(v1,v2)/(v1.norm*v2.norm))

def color_map(angle):
    return np.ceil(np.array(angle*255)/np.pi)

def rescale(value, max_val, max_rescaled):
    return (value*max_rescaled)/max_val


#test
def color_test():
    v1 = Vector(1,0,0)
    v2 = [Vector(np.random.randint(0,30),np.random.randint(0,30),np.random.randint(0,30)) for z in range(0,300)]
    dot1 = []
    dot2 = []
    k = 7
    max_vals = []
    for vec in v2:
        max_vals.append(color_map(relative_direction(v1,vec)**k))
    max_val = np.max(max_vals)
    print(np.max(max_vals))
    print(max_val)
    for vec in v2:
        d1 = color_map(relative_direction(v1,vec))
        d2 = color_map(rescale(relative_direction(v1,vec)**k,max_val,255))
        print("Standard dot {} ".format(d1))
        print("Sensitive dot {} ".format(d2))
        print("\n")
        dot1.append(d1)
        dot2.append(d2)
    print("PARAMETERS \n")
    print(np.max(dot1), np.max(dot2))
    print(np.min(dot1), np.min(dot2))
    print(np.median(dot1), np.mean(dot1), np.std(dot1))
    print(np.median(dot2), np.mean(dot2), np.std(dot2))

#color_test()
