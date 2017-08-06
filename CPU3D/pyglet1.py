from PyQt4 import QtGui, QtCore
import pyglet
pyglet.options['debug_gl'] = False
from pyglet.gl import *
from pyglet.window import key, mouse
from OpenGL.GLUT import *
from CPU3D.camera_calculations import *
import pathlib
import numpy as np

WINDOW = 700
INCREMENT = 5

class Window(pyglet.window.Window):
    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.initial_transformation()
        self.i = 0
        self.cl = True  # this variable provides color inversion
        self.cube = True
        self.spacer = 1.5
        self.round = False
        self.record = True
        if self.record:
            self.name = "./<Magnetization>/"
            pathlib.Path(self.name).mkdir(parents=True, exist_ok=True)
        self.last_i = 34
        self.first_i = 21
        self.label = self.customText("Magnetoresistance")

    def customText(self, text):
        label = pyglet.text.Label(text, font_name='TimesNewRoman',
                    font_size=11, x=10, y=-20, anchor_x='left', \
                    anchor_y='top', color=(100,250,100,255))
        return label

    def getDataFromRunner(self, data):
        self.vectors_list = data[0]
        self.color_list = data[1]
        self.iterations = data[2]
        self.control = data[3]
        self.fps_display = data[4]
        self.av = data[5]

    def upload_uniforms(self):
        uni = self.shader.uniforms

        uni.view = translate(None, tuplqe(self.position))

        mod_mat = rotate(None, self.rotation[0], (1.0, 0.0, 0.0))
        mod_mat = rotate(mod_mat, self.rotation[1], (0.0, 1.0, 0.0))
        uni.model = rotate(mod_mat, self.rotation[2], (0.0, 0.0, 1.0))

        width, height = self.get_size()
        uni.proj = perspective(60.0, width / height, 0.1, 256.0)

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

    def draw_cube(self, vec, color=[1,0,1], a=[1,1,0], b= [-1,-1,0]):
        glBegin(GL_QUADS)
        #TOP FACE
        #glColor3f(color[0], color[1],color[2])
        glColor3f(np.dot(a, color), np.dot(b, color), 0)
        glVertex3f(vec[3]+self.spacer, vec[4], vec[5]+self.spacer)
        glVertex3f(vec[3], vec[4], vec[5]+self.spacer)
        glVertex3f(vec[3], vec[4]+self.spacer, vec[5]+self.spacer)
        glVertex3f(vec[3]+self.spacer, vec[4]+self.spacer, vec[5]+self.spacer)
        #BOTTOM FACE
        glColor3f(np.dot(a, color), np.dot(b, color), 0)
        #glColor3f(color[0], color[1],color[2])
        glVertex3f(vec[3]+self.spacer, vec[4], vec[5])
        glVertex3f(vec[3], vec[4], vec[5])
        glVertex3f(vec[3], vec[4]+self.spacer, vec[5])
        glVertex3f(vec[3]+self.spacer, vec[4]+self.spacer, vec[5])
        #FRONT FACE
        glColor3f(np.dot(a, color), np.dot(b, color), 0)
        #glColor3f(color[0], color[1],color[2])
        glVertex3f(vec[3]+self.spacer, vec[4]+self.spacer, vec[5]+self.spacer)
        glVertex3f(vec[3], vec[4]+self.spacer, vec[5]+self.spacer)
        glVertex3f(vec[3], vec[4]+self.spacer, vec[5])
        glVertex3f(vec[3]+self.spacer, vec[4]+self.spacer, vec[5])
        #BACK FACE
        glColor3f(np.dot(a, color), np.dot(b, color), 0)
        #glColor3f(color[0], color[1],color[2])
        glVertex3f(vec[3]+self.spacer, vec[4], vec[5]+self.spacer)
        glVertex3f(vec[3], vec[4], vec[5]+self.spacer)
        glVertex3f(vec[3], vec[4], vec[5])
        glVertex3f(vec[3]+self.spacer, vec[4], vec[5])
        #RIGHT FACE
        glColor3f(np.dot(a, color), np.dot(b, color), 0)
        #glColor3f(color[0], color[1],color[2])
        glVertex3f(vec[3]+self.spacer, vec[4], vec[5]+self.spacer)
        glVertex3f(vec[3]+self.spacer, vec[4]+self.spacer, vec[5]+self.spacer)
        glVertex3f(vec[3]+self.spacer, vec[4]+self.spacer, vec[5])
        glVertex3f(vec[3]+self.spacer, vec[4], vec[5])
        #LEFT FACE
        glColor3f(np.dot(a, color), np.dot(b, color), 0)
        #glColor3f(color[0], color[1],color[2])
        glVertex3f(vec[3], vec[4]+self.spacer, vec[5]+self.spacer)
        glVertex3f(vec[3], vec[4], vec[5]+self.spacer)
        glVertex3f(vec[3], vec[4], vec[5])
        glVertex3f(vec[3], vec[4]+self.spacer, vec[5])
        glEnd()

    def draw_cordinate_system(self, size=5):
        self.draw_vector([0, 0, 0, size, 0, 0], [1, 0, 0]) #x
        self.draw_vector([0, 0, 0, 0, size, 0], [0, 1, 0]) #y
        self.draw_vector([0, 0, 0, 0, 0, size], [0, 0, 1]) #z

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
        self.fps_display.draw()
        self.label.draw()
        pyglet.text.Label(str(self.i), font_name='Comic Sans',
                    font_size=11, x=10, y=-20, anchor_x='right', \
                    anchor_y='bottom', color=(100,100,100,255)).draw()
        for vector, color in zip(self.vectors_list[0::self.av], \
                                                self.colors[0::self.av]):
            if self.cl:
                color = color[::-1]
            if not self.cube: self.draw_vector(vector, color=color)
            if self.cube: self.draw_cube(vector, color=color)
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
        self.colors = self.color_list[self.i]

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # SMART SCROLL BETA
        self.position[0] -= mt.sin(self.rotation[0] * mt.pi / 180) * \
                            mt.cos(self.rotation[1] * mt.pi / 180) * scroll_y
        self.position[1] += mt.cos(self.rotation[0] * mt.pi / 180) * \
                            mt.sin(self.rotation[1] * mt.pi / 180) * scroll_y
        self.position[2] += mt.cos(self.rotation[0] * mt.pi / 180) * \
                            mt.cos(self.rotation[1] * mt.pi / 180) * scroll_y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT != 0:
            rotation_speed = 0.5
            self.rotation[0] += dx * rotation_speed
            xpos = self.position[0] * mt.cos(dx * rotation_speed * mt.pi / 180)\
                - self.position[2] * mt.sin(dx * rotation_speed * mt.pi / 180)
            zpos = self.position[0] * mt.sin(dx * rotation_speed * mt.pi / 180)\
                + self.position[2] * mt.cos(dx * rotation_speed * mt.pi / 180)

            self.position[0] = xpos
            self.position[2] = zpos

        elif buttons & mouse.RIGHT != 0:
            self.position[0] += dx * 0.1
            self.position[1] += dy * 0.1

    #DO NOT REMOVE dt FROM ARGUMENTS OTHERWISE IT WOULD NOT RUN
    def update(self, dt):
        if self.record:
            if not self.round: self.save_current_window()
            if self.i == self.iterations-1: self.round = True
        self.on_resize(self.width, self.height)

    def save_current_window(self):
        if self.i <= self.last_i and self.i >= self.first_i:
            print("Saved {}".format(self.i))
            pyglet.image.get_buffer_manager().get_color_buffer().save(self.name +
                                                "mag_py_" + str(self.i)+".jpg")
