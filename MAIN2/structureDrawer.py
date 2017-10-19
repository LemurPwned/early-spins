from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

from PyQt5.QtWidgets import QWidget, QLabel

class DrawData():
    def __init__(self):
        self.rotation = [0,0,0]
        self.position = [0,-1,-10]
        self.initialRun = True

    def draw_vector(self, vec, color=[0, 0, 0], a=[1,1,0], b= [-1,-1,0]):
        # [1,1,0] x, y ,z - red
        # [-1,-1,0] x, y, z - blue
        glLineWidth(3)
        #glColor3f(color[0], color[1], color[2])
        glColor3f(np.dot(a, color), np.dot(b, color), 0)
        glBegin(GL_LINES)
        glVertex3f(vec[0], vec[1], vec[2])
        glVertex3f(vec[3]+color[0], vec[4]+color[1], vec[5]+color[2])
        glEnd()
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex3f(vec[3]+color[0], vec[4]+color[1], vec[5]+color[2])
        glEnd()

    def draw_cordinate_system(self, size=5):
        self.draw_vector([0, 0, 0, size, 0, 0], [1, 0, 0]) #x
        self.draw_vector([0, 0, 0, 0, size, 0], [0, 1, 0]) #y
        self.draw_vector([0, 0, 0, 0, 0, size], [0, 0, 1]) #z'''

    def cameraLeft(self):
        self.rotation[0] += 5

    def cameraRight(self):
        self.rotation[0] -= 5

    def initialSettings(self):
        self.position = [0, -1, -10]

    def paintGL(self):
        '''testing purposes'''
        glClear(GL_COLOR_BUFFER_BIT)
        self.draw_cordinate_system(5)
        if self.initialRun:
            self.initialSettings()
            gluPerspective(90, 651/551, 0.1, 50.0)
            self.initialRun = False


        glTranslate(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation[0], 0, 1, 0)  # weird
        glRotatef(self.rotation[1], 1, 0, 0)  # weird
        glRotatef(self.rotation[2], 0, 0, 1)
        self.position = [0,0,0]
        self.rotation = [0,0,0]
        #self.cameraLeft()

        #glTranslatef(0, -1, -10)
