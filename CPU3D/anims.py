import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
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
        self.i = 0
        self.graph_data = []
        self.null_data = []
        self.title = 'Magnetization'
        self.canvas_type = None

    def reshape_data(self):
        '''
        reshaping the data so that plotting might happen faster
        '''
        xc = int(self.base_data['xnodes'])
        yc = int(self.base_data['ynodes'])
        zc = int(self.base_data['znodes'])
        self.layers_data = np.array([x.reshape(zc,yc*xc,3)[self.current_layer] for x in self.tdata])
        self.current_single_layer = np.array([calculate_angles(x)
                                for x in self.layers_data])
        x = np.linspace(0, xc, xc)
        y = np.linspace(0, yc, yc)
        self.dx, self.dy = np.meshgrid(x,y)

    #INDEPENDENT graph_panels
    def create_plot_canvas(self):
        self.canvas_type = 'panel'
        self.fig = plt.figure()
        self.fig.suptitle(self.title)
        self.ax_pl = plt.subplot(111)
        self.i = self.i
        self.null_data = [x for x in range(self.iterations)]
        a_handler = self.ax_pl.plot(self.null_data,
            self.graph_data[0:self.i]+self.null_data[self.i:], 'ro')[0]
        self.ax_pl.hpl = a_handler
        self.ax_pl.axis([0, self.iterations, np.min(self.graph_data), np.max(self.graph_data)])
        self.ax_pl.set_autoscale_on(False)
        self.ax_pl.set_title('{}/{}'.format(self.i,self.iterations))

    def replot(self):
        self.ax_pl.hpl.set_ydata(self.graph_data[0:self.i]+self.null_data[self.i:])
        self.ax_pl.set_title('{}/{}'.format(self.i, self.iterations))
        self.ax_pl.get_figure().canvas.draw()

    #WIDGETS
    def create_button_canvas(self, title='Magnetization'):
        self.canvas = 'widget'
        self.fig = plt.figure()
        self.fig.suptitle(self.title)
        self.ax_pl = plt.subplot(111)
        self.ax_pl = plt.subplot2grid((5,5),(0,0),colspan=5,rowspan=3)  # axes_plot
        self.ax_bl = plt.subplot2grid((5,5),(4,0),colspan=2,rowspan=1)  # axes_button_left
        self.ax_br = plt.subplot2grid((5,5),(4,3),colspan=2,rowspan=1)  # axes_button_right
        self.butt_l = Button(self.ax_bl, '\N{leftwards arrow}')
        self.butt_r = Button(self.ax_br, '\N{rightwards arrow}')
        self.i = self.i
        scat = self.ax_pl.scatter(self.dx, self.dy,
                            c=tuple(self.current_single_layer[self.i]), cmap=cm.jet)
        self.ax_pl.hpl = scat
        self.fig.colorbar(self.ax_pl.hpl)
        self.ax_pl.axis('scaled')
        self.ax_pl.axis([0, len(self.dx), 0, len(self.dy)])
        self.ax_pl.set_autoscale_on(False)
        self.ax_pl.set_title('{}/{}'.format(self.i,self.current_single_layer.shape[0]-1))

    def create_canvas(self, title='Magnetization'):
        self.fig = plt.figure()
        self.fig.suptitle(self.title)
        self.ax_pl = plt.subplot(111)
        self.i = self.i
        scat = self.ax_pl.scatter(self.dx, self.dy,
                            c=tuple(self.current_single_layer[self.i]), cmap=cm.jet)
        self.ax_pl.hpl = scat
        self.fig.colorbar(self.ax_pl.hpl)
        self.ax_pl.axis('scaled')
        self.ax_pl.axis([0, len(self.dx), 0, len(self.dy)])
        self.ax_pl.set_autoscale_on(False)
        self.ax_pl.set_title('{}/{}'.format(self.i,self.current_single_layer.shape[0]-1))

    def replot_data(self):
        self.ax_pl.hpl.set_array(self.current_single_layer[self.i])
        self.ax_pl.set_title('{}/{}'.format(self.i,
                self.current_single_layer.shape[0]-1))
        self.ax_pl.get_figure().canvas.draw()

    def replot_call(self):
        """
        verifies the instance of canvas and calls correct replot
        """
        if self.canvas_type == 'widget':
            self.replot_data()
        elif self.canvas_type == 'panel':
            self.replot()

    def left_cl(self, event):
        if self.i > 0:
            self.i -= 1
            self.replot_data()
        if self.i == 0:
            self.i = self.current_single_layer.shape[0]-1
            self.replot_data()

    def right_cl(self, event):
        if self.i < self.current_single_layer.shape[0]-1:
            self.i += 1
            self.replot_data()
        if self.i == self.current_single_layer.shape[0]-1:
            self.i = 0
            self.replot_data()

    def run_canvas(self):
        plt.show()

    def run_button_canvas(self):
        self.butt_l.on_clicked(self.left_cl)
        self.butt_r.on_clicked(self.right_cl)
        plt.show()

    #ANIMATIONS
    def onPress(self, event):
        if self.anim_running:
            self.ani.event_source.stop()
            self.anim_running = False
        else:
            self.ani.event_source.start()
            self.anim_running = True

    def init_anim(self, title='Animation'):
        fig = plt.figure()
        c = self.current_single_layer[0]
        scat = plt.scatter(self.dx, self.dy,
                            c=tuple(c), cmap=cm.jet)
        fig.suptitle(self.title)
        fig.colorbar(scat)
        fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.ani = animation.FuncAnimation(fig, update,
                    frames=range(self.iterations),
                    fargs=(self.current_single_layer, scat),
                    interval=self.TIME_INTERVAL)
        plt.show()

def update(i, current_single_layer, scat):
    scat.set_array(np.array(current_single_layer[i],
                            dtype=float))
    return scat

def calculate_angles(x, relate = [0,1,0], scale=1):
    #TODO: make relate object a variable
    norm = np.apply_along_axis(np.linalg.norm, 1, x)
    dot = np.divide(np.array([np.inner(i, relate) for i in x]), norm)
    angle = np.arccos(dot)**scale
    angle[np.isnan(angle)] = -1
    return angle
