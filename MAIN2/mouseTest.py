from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
window = 0												# glut window number

# initial position of the rectangle
'''rect_x = 0
rect_y = 200

# constants
RECT_WIDTH = 50
RECT_HEIGHT = 50
RECT_DELAY = 20
width, height = 400, 400								# width and height of the window
dx = 0													# direction to x
dy = 0													# direction to y
mouse_y = 0												# position of mouse cursor to x
mouse_x = 0												# position of mouse cursor to y
s = 1													# path
v = 3													# speed of movement of the ball

# window size
def draw_rect(x, y, width, height):
	glBegin(GL_QUADS)									# start drawing a rectangle
	glVertex2f(x, y)									# bottom left point
	glVertex2f(x + width, y)							# bottom right point
	glVertex2f(x + width, y + height)					# top right point
	glVertex2f(x, y + height)							# top left point
	glEnd()

def refresh2d(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()
'''
def draw():												# ondraw is called all the time
	pass
	'''glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# clear the screen
	glLoadIdentity()									# reset position

	# ToDo draw rectangle
	refresh2d(width, height)
	glColor3f(0.0, 0.0, 2.0)
	draw_rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
	glutSwapBuffers()									# important for double buffering
'''


def mouseControl( mx, my):

	#global rect_x, rect_y, dx, dy, s, mouse_x, mouse_y

	#my_new = height - my
	#mouse_x = mx
	#mouse_y = my_new

	'''dif_x = mx - rect_x									# differnce between position of mouse cursor and rectangle to x
	dif_y = my_new - rect_y								# differnce between position of mouse cursor and rectangle to y

	s = math.sqrt(dif_x ** 2 + dif_y ** 2)
	k = v / s
	#k=0
	dx = k * dif_x
	dy = k * dif_y'''
	print(mx, my)


'''def movement(value):

	global rect_x, rect_y, mouse_x, mouse_y

	rect_x += dx
	rect_y += dy

	dif_x_new = mouse_x - rect_x							# new differnce between position of mouse cursor and rectangle to x while rectangle is going
	dif_y_new = mouse_y - rect_y							# new differnce between position of mouse cursor and rectangle to y while rectangle is going
	step_s = math.sqrt( dif_x_new ** 2 +  dif_y_new ** 2)	# path changed all the time when rectangle approaches to mouse cursor

# stop move when rectangle is on the cursor position
	if int(step_s) <= v:
		rect_x = mouse_x
		rect_y = mouse_y

	glutTimerFunc(RECT_DELAY, movement, 0)

	'''

def paintGL():
	# initialization
	glutInit()												# initialize glut
	#glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	#glutInitWindowSize(800, 600)						# set window size
	#glutInitWindowPosition(10, 0)							# set window position
	window = glutCreateWindow("Approaching rectangle")				# create window with title
	glutDisplayFunc(draw)									# set draw function callback
	glutIdleFunc(draw)										# draw all the time
	glutPassiveMotionFunc(mouseControl)
	#glutTimerFunc(RECT_DELAY, movement, 0)
	glutMainLoop()

if __name__ == "__main__":
	paintGL()
