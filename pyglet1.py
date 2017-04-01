import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from OpenGL.GLUT import *
from input_parser import *
import pandas as pd
import tiny_vectors as vc
import math as mt
from camera_calculations import *


WINDOW   = 800
INCREMENT = 5
colors = []
class Window(pyglet.window.Window):

    #xRotation = yRotation = 30

    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.initial_transformation()
        self.i = 0

    def upload_uniforms(self):
        uni = self.shader.uniforms

        uni.view = translate(None, tuple(self.position) )

        mod_mat = rotate(None, self.rotation[0], (1.0, 0.0, 0.0))
        mod_mat = rotate(mod_mat, self.rotation[1], (0.0, 1.0, 0.0))
        uni.model = rotate(mod_mat, self.rotation[2], (0.0, 0.0, 1.0))

        width, height = self.get_size()
        uni.proj = perspective(60.0, width/height, 0.1, 256.0)

    def draw_vector(self, vec, color=(1,1,1)):
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
        step = 1
        xk = 2
        yk = 3
        zk = 3
        angles = []
        for index, row in df.iterrows():
            #if iterator%10 == 0:
            if skip%step == 0:
                if xpos>=int(base_data['xnodes']):
                    ypos+=1+(xpos%int(base_data['xnodes']))
                    xpos=0
                if ypos>=int(base_data['ynodes']):
                    zpos+=1+(ypos%int(base_data['ynodes']))
                    ypos=0
                    xpos=0

                xpos+=1*step
                xtemp = xpos*float(base_data['xbase'])*1e9
                ytemp = ypos*float(base_data['ybase'])*1e9
                ztemp = zpos*float(base_data['zbase'])*1e9
                c = vc.Vector(row[0],row[1],row[2])

                if np.abs(row[0]+row[1]+row[2]) > 0:
                    self.vec.append([xtemp, ytemp, ztemp, xtemp+row[0]/c.norm,
                                        ytemp+row[1]/c.norm, ztemp+row[2]/c.norm])
                    angles.append((vc.relative_direction(c, b1)**(2*xk + 1),
                                    vc.relative_direction(c, b2)**(2*yk + 1),
                                    vc.relative_direction(c, b3)**(2*zk + 1)))
                else:
                    continue
            skip += 1
        print(count)
        xmax = 0
        ymax = 0
        zmax = 0
        for angle in angles:
            if xmax < np.abs(angle[0]):
                xmax = np.abs(angle[0])
            if ymax < np.abs(angle[1]):
                ymax = np.abs(angle[1])
            if zmax < np.abs(angle[2]):
                zmax = np.abs(angle[2])

        for angle in angles:
            colors.append((vc.rescale((angle[0]/xmax),xmax,255)*(10**(xk-1))/255,
                            vc.rescale((angle[1]/ymax),ymax,255)*(10**(yk-1))/255,
                            vc.rescale((angle[2]/zmax),zmax,255)*(10**(zk-1))/255))
        #print(colors)

    def initial_transformation(self):
        self.rotation = [0,0,0] #xyz degrees in xyz axis
        self.position = [0,0,-10] #xyz initial
        #self.pointing = [0,0,0] #where camera points

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
        #x=0

        for vector, color in zip(self.vec, colors):
            self.draw_vector(vector, color=color)
        # Pop Matrix off stack
        glPopMatrix()
        print(self.position, self.rotation)

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
        #SMART SCROLL BETA
        self.position[0] -= mt.sin(self.rotation[0]*mt.pi/180)*mt.cos(self.rotation[1]*mt.pi/180)*scroll_y
        self.position[1] += mt.cos(self.rotation[0]*mt.pi/180)*mt.sin(self.rotation[1]*mt.pi/180)*scroll_y
        self.position[2] += mt.cos(self.rotation[0]*mt.pi/180)*mt.cos(self.rotation[1]*mt.pi/180)*scroll_y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT != 0:

            #self.rotation[0] -= dx * 0.06
            rotation_speed = 0.5
            self.rotation[0] += dx*rotation_speed
            #self.rotation[1] -= dy
            #temp = xpos
            xpos = self.position[0] * mt.cos(dx*rotation_speed * mt.pi / 180) - self.position[2] * mt.sin(dx*rotation_speed * mt.pi / 180)
            zpos = self.position[0] * mt.sin(dx*rotation_speed * mt.pi / 180) + self.position[2] * mt.cos(dx*rotation_speed * mt.pi / 180)

            #ypos = self.position[1] * mt.cos(dy * mt.pi / 180) - self.position[2] * mt.sin(dy * mt.pi / 180)
            #zpos = self.position[1] * mt.sin(dy * mt.pi / 180) + self.position[2] * mt.cos(dy * mt.pi / 180) + self.position[0] * mt.sin(dx * mt.pi / 180)

            self.position[0] = xpos
            #self.position[1] = ypos
            self.position[2] = zpos


            #self.rotation[0] +=

            #self.rotation[1] += dy * 0.06
            #self.position[0] += dx * 0.006
            #self.position[1] += dy * 0.006
        elif buttons & mouse.RIGHT != 0:
            self.position[0] += dx * 0.1
            self.position[1] += dy * 0.1
            #self.pointing[0] += dx * 0.1
            #self.pointing[2] += dy * 0.1

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.change_frame()

    def change_frame(self):
        self.i += 1
        print(self.i)
        data = tdata[self.i]
        base_data = tbase_data[self.i]
        count = tcount[self.i]

def getAllFiles(directory, format):
    #format = ".omf"
    #directory = "./data/"
    tFileList = os.listdir(directory)
    # print(tFileList[0])
    fileList = []
    for file in tFileList:
        # print(file)
        if file.find(format) != -1:
            fileList.append(directory + file)

    #print(fileList)
    i = 0
    base_data = []
    count = []
    data = []
    print("Reading data...")
    for file in fileList:
        tbase_data, tcount = extract_base_data(file)
        base_data.append(tbase_data)
        count.append(tcount)
        to_skip = [x for x in range(tcount)]
        data.append(form_dataframe(file, to_skip))

    return data, base_data, count

if __name__ == '__main__':

    tdata, tbase_data, tcount = getAllFiles("./data/", ".omf")
    data = tdata[0]
    base_data = tbase_data[0]
    count = tcount[0]
    #i=0
    Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
    pyglet.app.run()
