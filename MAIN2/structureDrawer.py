from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def paintGL():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1,0,0);
    glBegin(GL_TRIANGLES);
    glVertex3f(-0.5,-0.5,0);
    glVertex3f(0.5,-0.5,0);
    glVertex3f(0.0,0.5,0);
    glEnd()

    gluPerspective(45, 651/551, 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)
