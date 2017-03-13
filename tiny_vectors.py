import numpy as np

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.norm = np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def set_color(self, color):
        self.color = color

def dot(v1,v2):
        return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z

def relative_direction(v1, v2=Vector(1,0,0)):
        return np.arccos(dot(v1,v2)/(v1.norm*v2.norm))

def color_mapping(angle1, angle2, angle3, scale=1):
        #r - v1, g - v2, b - v3
        if angle1 > 0:
            r = np.ceil(np.array(angle1*255/scale)/np.pi)
        else:
            r = 0
        if angle2 > 0:
            g = np.ceil(np.array(angle2*255/scale)/np.pi)
        else:
            g = 0
        if angle3 > 0:
            b = np.ceil(np.array(angle3*255/scale)/np.pi)
        else:
            b = 0
        return (r,g,b)

def color_map(angle):
        # red is (255,0,0); yellow is (255,255,0) will turn yellow->red
        if angle<0:
            return 0
        else:
            new_map = np.ceil(np.array(angle*255)/np.pi)
            return new_map

#test
