import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from OpenGL.GLUT import *
from input_parser import *
import tiny_vectors as vc
from camera_calculations import *
from graph_panels import calculate_angle, generate_color_series

WINDOW = 800
INCREMENT = 5
colors = []
dataX = []


class Window(pyglet.window.Window):
    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.initial_transformation()
        self.i = 0

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
        self.draw_vector([0, 0, 0, size, 0, 0], [1, 0, 0])
        self.draw_vector([0, 0, 0, 0, size, 0], [0, 1, 0])
        self.draw_vector([0, 0, 0, 0, 0, size], [0, 0, 1])

    def create_vector(self, df):
        print("Mean of data in create_vector", np.mean(df['x']))
        self.vec = []
        # this version assumes just one magnetization direction at the time
        xpos = 0
        ypos = 0
        zpos = 0
        skip = 0
        # pick just one vector at the time
        b1 = vc.Vector(1, 0, 0)
        b2 = vc.Vector(0, 1, 0)
        b3 = vc.Vector(0, 0, 1)
        step = 1
        angles = []
        # power is proportional to the variance
        power = 35

        for index, row in df.iterrows():
            if skip % step == 0:
                if xpos >= int(base_data['xnodes']):
                    ypos += 1 + (xpos % int(base_data['xnodes']))
                    xpos = 0
                if ypos >= int(base_data['ynodes']):
                    zpos += 1 + (ypos % int(base_data['ynodes']))
                    ypos = 0
                    xpos = 0

                xpos += 1 * step
                xtemp = xpos * float(base_data['xbase']) * 1e9
                ytemp = ypos * float(base_data['ybase']) * 1e9
                ztemp = zpos * float(base_data['zbase']) * 1e9
                c = vc.Vector(row[0], row[1], row[2])

                if np.abs(row[0] + row[1] + row[2]) > 0:
                    self.vec.append([xtemp, ytemp, ztemp, xtemp + row[0] / c.norm,
                                     ytemp + row[1] / c.norm, ztemp + row[2] / c.norm])
                    angles.append(np.power(vc.relative_direction(c, b1), power))
                else:
                    continue
            skip += 1
        max_angle = np.max(angles)
        print(max_angle)

        print("Mean of angles: ", np.mean(angles))
        series = generate_color_series(len(angles))
        temp_color = [x for (y, x) in sorted(zip(angles, series))]
        # repopulate color in a global scope
        del colors[:]
        for color in temp_color:
            colors.append(color)
        # for angle in angles:
            # colors.append((angle/max_angle, angle/max_angle, angle/max_angle))

    def initial_transformation(self):
        self.rotation = [0, 0, 0]  # xyz degrees in xyz axis
        self.position = [0, 0, -10]  # xyz initial
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
        # x=0

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
        self.create_vector(data[self.i])

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

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.change_frame()

    def change_frame(self):
        self.i += 1
        print(self.i)
        base_data = tbase_data[self.i]
        count = tcount[self.i]
        width, height = self.get_size()
        print(colors)
        print("Mean of colors ", np.mean(colors))
        print("Mean of data in change frame: ", np.mean(data[self.i]['x']))
        self.on_resize(width, height)


def getAllFiles(directory, format):
    tFileList = os.listdir(directory)
    fileList = []
    for file in tFileList:
        # print(file)
        if file.find(format) != -1:
            fileList.append(directory + file)

    base_data = []
    count = []
    data = []
    print("Reading data...")
    fileList.sort()
    for file in fileList:
        tbase_data, tcount = extract_base_data(file)
        base_data.append(tbase_data)
        count.append(tcount)
        to_skip = [x for x in range(tcount)]
        data.append(form_dataframe(file, to_skip))

    return data, base_data, count


if __name__ == '__main__':
    tdata, tbase_data, tcount = getAllFiles("./data/", ".omf")
    data = tdata
    print(len(dataX))
    base_data = tbase_data[0]
    count = tcount[0]
    Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
    pyglet.app.run()
