import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from OpenGL.GLUT import *

WINDOW   = 800
INCREMENT = 5

class Window(pyglet.window.Window):

    # Cube 3D start rotation
    xRotation = yRotation = 30  

    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)

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
        for vec in arr:
            #print(vec)
            #glPointSize(1)
            glBegin(GL_LINES)
            glVertex3f(vec[0],vec[1],vec[2])
            glVertex3f(vec[3],vec[4],vec[5])
            glEnd()
            glPointSize(3)
            glBegin(GL_POINTS)
            glVertex3f(vec[3],vec[4],vec[5])
            glEnd()
            

    def create_vector(self):
        self.vec = []
        for i in range(-30, 30):
            for j in range(-30, 30):
                self.vec.append([i, j, 0, i, j, 1])        
    
    def on_draw(self):
        # Clear the current GL Window
        self.clear()

        # Push Matrix onto stack
        glPushMatrix()

        glRotatef(self.xRotation, 1, 0, 0)
        glRotatef(self.yRotation, 0, 1, 0)

        # Draw the six sides of the cube
        
        
        #self.draw_vector([[0,0,0,4,0,0],[0,0,0,0,4,0], [0,0,0,0,0,4]])
        self.draw_vector(self.vec)
        '''for i in range(-40,40):
            glColor3ub(i*2, 150, 100)
            for j in range(-40, 40):
                glVertex3f(i*5,j*5,0)
                glVertex3f(i*5,j*5,5)'''
        

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
        self.create_vector()


    '''def on_text_motion(self, motion):
        if motion == key.UP:
            self.xRotation -= INCREMENT
        if motion == key.DOWN:
            self.xRotation += INCREMENT
        if motion == key.LEFT:
            self.yRotation -= INCREMENT
        if motion == key.RIGHT:
            self.yRotation += INCREMENT
            '''

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.position[2] -= 0.3*scroll_y
        #self.upload_uniforms()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT != 0:
            self.xRotation -= dy * 0.3
            self.yRotation += dx * 0.3
        elif buttons & mouse.RIGHT != 0:
            self.position[0] += dx * 0.005
            self.position[1] += dy * 0.005


            
if __name__ == '__main__':
    Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
    pyglet.app.run()
