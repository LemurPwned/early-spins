import math as mt
import numpy as np

def rotate(x, y, z, t, p, f):
    rotationMatrix = np.matrix([[mt.cos(t*mt.pi/180)*mt.cos(p*mt.pi/180), mt.cos(f*mt.pi/180)*mt.sin(p*mt.pi/180) + mt.sin(f*mt.pi/180)*mt.sin(t*mt.pi/180)*mt.cos(p*mt.pi/180), mt.sin(f*mt.pi/180)*mt.sin(p*mt.pi/180) - mt.cos(f*mt.pi/180)*mt.sin(t*mt.pi/180)*mt.cos(p*mt.pi/180)],
                           [-mt.cos(t*mt.pi/180)*mt.sin(p*mt.pi/180), mt.cos(f*mt.pi/180)*mt.cos(p*mt.pi/180) + mt.sin(f*mt.pi/180)*mt.sin(t*mt.pi/180)*mt.sin(p*mt.pi/180), mt.sin(f*mt.pi/180)*mt.cos(p*mt.pi/180) - mt.cos(f*mt.pi/180)*mt.sin(t*mt.pi/180)*mt.sin(p*mt.pi/180)],
                           [-mt.sin(t*mt.pi/180), -mt.sin(f*mt.pi/180)*mt.cos(t*mt.pi/180), -mt.cos(f*mt.pi/180)*mt.cos(t*mt.pi/180)]], dtype='f')

    temp = np.array([[x], [y], [z]])

    #print(rotationMatrix)
    temp = rotationMatrix*temp

    return temp.item(0), temp.item(1), temp.item(2)

def move(x, y, z, a1, a2):
    print(x,y,z,a1)
    dx = mt.cos(mt.radians(a1))
    dy = mt.sin(mt.radians(a1))
    print(dx, dy)

if __name__=="__main__":
    move(0,0,0,180,0)

