from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

from PyQt5.QtCore import QPoint

class DrawData():
    def __init__(self):
        pass

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

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        '''if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()    '''

    #@staticmethod
    def paintGL(self):
        '''testing purposes'''
        glClear(GL_COLOR_BUFFER_BIT)
        self.draw_cordinate_system(5)
        '''for i in range(3):
            glColor3f(1,0,0);
            glBegin(GL_TRIANGLES);

            glVertex3f(-0.5,-0.5,i);
            glVertex3f(0.5,-0.5,0);
            glVertex3f(0.0,0.5,0);
            glEnd()'''

        gluPerspective(90, 651/551, 0.1, 50.0)
        glTranslatef(0, -1, -10)
