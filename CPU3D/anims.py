import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import time as tm

class Animation():
    def __init__(self):
        self.current_layer = 0
        self.base_data = []
        self.tdata = []
        self.layers_data = []
        self.current_single_layer = []
        self.dx = []
        self.dy = []
        self.iterations = 0
        self.anim_running = True
        self.TIME_INTERVAL = 200
        self.backwards_counter = 0
        self.i = 0
        self.play = True

    def onPress(self, event):
        if self.anim_running:
            self.ani.event_source.stop()
            self.anim_running = False
        else:
            self.ani.event_source.start()
            self.anim_running = True

    def reshape_data(self):
        xc = int(self.base_data['xnodes'])
        yc = int(self.base_data['ynodes'])
        zc = int(self.base_data['znodes'])
        self.layers_data = np.array([x.reshape(zc,yc*xc,3)[self.current_layer] for x in self.tdata])
        self.current_single_layer = np.array([calculate_angles(x)
                                for x in self.layers_data])
        x = np.linspace(0, xc, xc)
        y = np.linspace(0, yc, yc)
        self.dx, self.dy = np.meshgrid(x,y)

    def init_anim(self, title='Animation'):
        fig = plt.figure()
        c = self.current_single_layer[0]
        scat = plt.scatter(self.dx, self.dy,
                            c=tuple(c), cmap=cm.jet)
        fig.suptitle(title)
        fig.colorbar(scat)
        fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.ani = animation.FuncAnimation(fig, update,
                    frames=range(self.iterations),
                    fargs=(self.current_single_layer, scat),
                    interval=self.TIME_INTERVAL)
        plt.show()

def update(i, current_single_layer, scat):
    print(i) #idk why works
    scat.set_array(np.array(current_single_layer[i],
                            dtype=float))
    return scat

def calculate_angles(x, relate = [0,1,0], scale=1):
    #TODO: make relate object variable
    norm = np.apply_along_axis(np.linalg.norm, 1, x)
    dot = np.divide(np.array([np.inner(i, relate) for i in x]), norm)
    angle = np.arccos(dot)**scale
    angle[np.isnan(angle)] = -1
    return angle
