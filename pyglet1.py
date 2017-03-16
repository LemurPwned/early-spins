import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from OpenGL.GLUT import *
from input_parser import *
import pandas as pd
import tiny_vectors as vc

WINDOW   = 800
INCREMENT = 5
colors = []
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

    def draw_vector(self, vec, color=[1,1,1]):
        #arr in format [[x1,x2,x3, y1,y2,y3], [], [], [], []...]
        #TODO create coloring algorithm
        #maybe multithreading?

        glColor3f(color[0], color[1], color[2])
        glBegin(GL_LINES)
        glVertex3f(vec[0],vec[1],vec[2])
        glVertex3f(vec[3],vec[4],vec[5])
        glEnd()
        glPointSize(3)
        glBegin(GL_POINTS)
        glVertex3f(vec[3],vec[4],vec[5])
        glEnd()

    def draw_cordinate_system(self, size = 5):
        self.draw_vector([0,0,0,size,0,0], [1,0,0])
        self.draw_vector([0,0,0,0,size,0], [0,1,0])
        self.draw_vector([0,0,0,0,0,size], [0,0,1])

    def create_vector(self, df):
        self.vec = []
        xpos = 0
        ypos = 0
        zpos = 0
        skip = 0
        count = 0
        b1 = vc.Vector(1,0,0)
        b2 = vc.Vector(0,1,0)
        b3 = vc.Vector(0,0,1)

        for index, row in df.iterrows():
            #if iterator%10 == 0:
            if skip%3 == 0:
                if xpos>=int(base_data['xnodes']):
                    ypos+=1
                    xpos=0
                if ypos>=int(base_data['ynodes']):
                    zpos+=1
                    ypos=0
                    xpos=0

                xpos+=1
                xtemp = xpos*float(base_data['xbase'])*1e9
                ytemp = ypos*float(base_data['ybase'])*1e9
                ztemp = zpos*float(base_data['zbase'])*1e9
                c = vc.Vector(row[0],row[1],row[2])
                if c.isZero != 1:
                    self.vec.append([xtemp, ytemp, ztemp, xtemp+row[0]/c.norm,
                                        ytemp+row[1]/c.norm, ztemp+row[2]/c.norm])

                    c = vc.Vector(row[0],row[1],row[2])
                    colors.append((vc.color_map(vc.relative_direction(c, b1))/255,
                                    vc.color_map(vc.relative_direction(c, b2))/255,
                                    vc.color_map(vc.relative_direction(c, b3))/255))
                else:
                    continue
            skip += 1
        print(count)


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
        self.draw_cordinate_system()
        x=0

        for vector, color in zip(self.vec, colors):
            self.draw_vector(vector, color=list(color))
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
