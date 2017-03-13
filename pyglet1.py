import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from OpenGL.GLUT import *
from input_parser import *
import pandas as pd

WINDOW   = 800
INCREMENT = 5

class Window(pyglet.window.Window):

    # Cube 3D start rotation
    xRotation = yRotation = 30

    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.initial_transformation()

    def upload_uniforms(self):
        uni = self.shader.uniforms

        uni.view = translate(None, tuple(self.position) )

        mod_mat = rotate(None, self.rotation[0], (1.0, 0.0, 0.0))
        mod_mat = rotate(mod_mat, self.rotation[1], (0.0, 1.0, 0.0))
        uni.model = rotate(mod_mat, self.rotation[2], (0.0, 0.0, 1.0))

        width, height = self.get_size()
        uni.proj = perspective(60.0, width/height, 0.1, 256.0)

    def draw_vector(self, arr):
        #arr in format [[x1,x2,x3, y1,y2,y3], [], [], [], []...]
        #TODO create coloring algorithm
        #maybe multithreading?
        for vec in arr:             #print(vec)
            #glPointSize(1)
            glBegin(GL_LINES)
            glVertex3f(vec[0],vec[1],vec[2])
            glVertex3f(vec[3],vec[4],vec[5])
            glEnd()
            glPointSize(3)
            glBegin(GL_POINTS)
            glVertex3f(vec[3],vec[4],vec[5])
            glEnd()

    def create_vector(self, df):
        self.vec = []
        iterator = df.shape[0]
        while iterator>1:
            row = next(df.iterrows())[1]
            if iterator%10 == 0:
                self.vec.append([row[0],row[1],row[2],1,0,iterator])
            iterator -= 1

    def form_vector_field(self, df):
        #should worry about the size
        iterator = df.shape[0]
        self.field = []
        while iterator>1:
            field.append([next(df.iterrows())[1][0],next(df.iterrows())[1][1],next(df.iterrows())[1][2],iterator,0,0])

    def initial_transformation(self):
        self.rotation = [0,0,0] #xyz degrees in xyz axis
        self.position = [0,0,-50] #xyz

    def transformate(self): #applies rotation and transformation
        glRotatef(self.rotation[0], 0, 1, 0)#weird
        glRotatef(self.rotation[1], 1, 0, 0)#weird
        glRotatef(self.rotation[2], 0, 0, 1)
        glTranslatef(self.position[0], self.position[1], self.position[2])

    def on_draw(self):
        # Clear the current GL Window
        self.clear()

        # Push Matrix onto stack
        glPushMatrix()

        self.transformate()

        self.draw_vector(self.vec)

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
        glTranslatef(0, 0, -50)
        self.create_vector(data)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.position[2] += 0.8*scroll_y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT != 0:
            self.rotation[0] += dx * 0.06
            self.rotation[1] -= dy * 0.06
        elif buttons & mouse.RIGHT != 0:
            self.position[0] += dx * 0.1
            self.position[1] += dy * 0.1




if __name__ == '__main__':
    filename = './data/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    base_data, count = extract_base_data(filename)
    to_skip = [x for x in range(count)]
    data = form_dataframe(filename, to_skip)

    Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
    pyglet.app.run()
