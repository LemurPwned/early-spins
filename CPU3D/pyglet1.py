from PyQt4 import QtGui, QtCore
import pyglet
pyglet.options['debug_gl'] = False
from pyglet.gl import *
pyglet.options['debug_gl'] = False
from pyglet.window import key, mouse
from OpenGL.GLUT import *
import time
from multiprocessing import Pool
import threading
from CPU3D.input_parser import *
from CPU3D.camera_calculations import *
from CPU3D.tiny_vectors import *
from CPU3D.graph_panels import calculate_angle, generate_color_series

WINDOW = 800
INCREMENT = 5
control = 30

TIME_INTERVAL = 1/60.0

class Window(pyglet.window.Window):

    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.initial_transformation()
        self.FREE_RUN = False
        self.i = 0

    def getDataFromRunner(self, data):
        self.vectors_list = data[0]
        self.color_list = data[1]
        self.tbase_data = data[2]
        self.header = data[3]


    def upload_uniforms(self):
        uni = self.shader.uniforms

        uni.view = translate(None, tuple(self.position))

        mod_mat = rotate(None, self.rotation[0], (1.0, 0.0, 0.0))
        mod_mat = rotate(mod_mat, self.rotation[1], (0.0, 1.0, 0.0))
        uni.model = rotate(mod_mat, self.rotation[2], (0.0, 0.0, 1.0))

        width, height = self.get_size()
        uni.proj = perspective(60.0, width / height, 0.1, 256.0)

    def draw_vector(self, vec, color=(1, 1, 1)):
        # arr in format [[x1,x2,x3, y1,y2,y3], [], [], [], []...]
        # TODO create coloring algorithm
        # maybe multithreading?
        glLineWidth(3)
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_LINES)
        glVertex3f(vec[0], vec[1], vec[2])
        glVertex3f(vec[3], vec[4], vec[5])
        glEnd()
        glPointSize(6)
        glBegin(GL_POINTS)
        glVertex3f(vec[3], vec[4], vec[5])
        glEnd()

    def draw_cordinate_system(self, size=5):
        self.draw_vector([0, 0, 0, size, 0, 0], [1, 0, 0]) #x
        self.draw_vector([0, 0, 0, 0, size, 0], [0, 1, 0]) #y
        self.draw_vector([0, 0, 0, 0, 0, size], [0, 0, 1]) #z

    #redundant function
    def create_vector(self, df):
        self.vec = vectors_list[self.i]
        self.colors = color_list[self.i]

    def initial_transformation(self):
        self.rotation = [0, 0, 0]  # xyz degrees in xyz axis
        self.position = [-10, -10, -40]  # xyz initial
        # self.pointing = [0,0,0] #where camera points

    def transformate(self):  # applies rotation and transformation
        glRotatef(self.rotation[0], 0, 1, 0)  # weird
        glRotatef(self.rotation[1], 1, 0, 0)  # weird
        glRotatef(self.rotation[2], 0, 0, 1)
        glTranslatef(self.position[0], self.position[1], self.position[2])

    def on_draw(self):
        # Clear the current GL Window
        self.clear()
        # Push Matrix onto stack
        glPushMatrix()
        self.transformate()
        self.draw_cordinate_system()
        for vector, color in zip(self.vec, self.colors):
            self.draw_vector(vector, color=color)
        # Pop Matrix off stack
        glPopMatrix()

    def on_resize(self, width, height):
        # set the Viewport
        glViewport(0, 0, width, height)
        # using Projection mode
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspectRatio = width / height
        gluPerspective(85, aspectRatio, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, 0)
        # TODO Replace create_vector with dataframe ops.
        #self.create_vector(data[self.i])
        self.vec = self.vectors_list[self.i]
        self.colors = self.color_list[self.i]

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # SMART SCROLL BETA
        self.position[0] -= mt.sin(self.rotation[0] * mt.pi / 180) * mt.cos(self.rotation[1] * mt.pi / 180) * scroll_y
        self.position[1] += mt.cos(self.rotation[0] * mt.pi / 180) * mt.sin(self.rotation[1] * mt.pi / 180) * scroll_y
        self.position[2] += mt.cos(self.rotation[0] * mt.pi / 180) * mt.cos(self.rotation[1] * mt.pi / 180) * scroll_y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT != 0:
            rotation_speed = 0.5
            self.rotation[0] += dx * rotation_speed
            xpos = self.position[0] * mt.cos(dx * rotation_speed * mt.pi / 180) - self.position[2] * mt.sin(
                dx * rotation_speed * mt.pi / 180)
            zpos = self.position[0] * mt.sin(dx * rotation_speed * mt.pi / 180) + self.position[2] * mt.cos(
                dx * rotation_speed * mt.pi / 180)

            self.position[0] = xpos
            self.position[2] = zpos

        elif buttons & mouse.RIGHT != 0:
            self.position[0] += dx * 0.1
            self.position[1] += dy * 0.1

    def next_frame(self):
        self.i+=1
        self.change_frame()

    def change_frame(self):
        self.list_guard()
        base_data = self.tbase_data[self.i]
        width, height = self.get_size()
        self.on_resize(width, height)

    #DO NOT REMOVE DF FROM ARGUMENTS OTHERWISE IT WOULD NOT RUN
    def update(self, df):
        if self.FREE_RUN:
            self.i += 1
            self.list_guard()
        self.change_frame()

    def list_guard(self):
        if self.i >= control-1:
            self.i = 0
        if self.i > self.header['Iteration'].count():
            self.i = 0
        else:
            pass
