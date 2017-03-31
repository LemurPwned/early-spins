import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
import tiny_vectors as vc


def callback_plotter(figures):
    '''
    allows for displaying figures produced by functions in this file
    '''

    if isinstance(figures, list):
        for fig in figures:
            fig.show()
            input('Press key to skip figure')
    else:
        figures.show()
        input('Press key to skip figure')

def plotters(data, pair, unit):
    '''
    pair is a tuple of strings.
    data is a dictionary
    pair argument is passed to specify what kind of plot pair should be generated
    e.g. pair('Iteration', 'Energy') would show Energy as function of Iteration
    '''
    fig = plt.figure()
    fig.suptitle('Direction : Magnetization')
    ax = fig.add_subplot(111)
    ax.plot(data[pair[0]], data[pair[1]])
    ax.set_xlabel(pair[0] + ' [' + unit[0]+']')
    ax.set_ylabel(pair[1] + ' [' + unit[1] + ']')
    return fig

def layer_splitter(data, base_data):
    '''
    data is DataFrame
    base_data is dictionary
    splits data into n separate layers with proper indices
    '''
    (x,y,z) = (int(base_data['xnodes']),int(base_data['ynodes']),int(base_data['znodes']))
    print(x,y,z)
    surface = x*y
    layers = [data.iloc[surface*i:surface*i + surface , :] for i in range(z)]
    #ask about the true layer size, should be divisible by 5
    #caveat, an artificial value is added to the last layer to make these equal
    layers[-1].loc[-1] = [0.0 for i in range(3)]
    return layers

def calculate_angle(data, relate):
    '''
    calculates the color of each vector
    '''
    norms = pd.Series(data['x']**2+data['y']**2+data['z']**2, dtype=np.float).apply(np.sqrt)
    dot = pd.Series(data['x']*relate.x+data['y']*relate.y+data['z']*relate.z, dtype=np.float)
    angle = pd.Series(dot/(relate.norm*norms), dtype=np.float).apply(np.arccos).fillna(np.float(-1))
    return angle

def color2d(data, base_vectors, base_data):
    '''
    this function maps layer and shows 2d plot for that layer
    show angular deviation from each base vectors
    will print 3 different plots for each
    '''
    angles = []
    sens = []
    norms = pd.Series(data['x']**2+data['y']**2+data['z']**2, dtype=np.float).apply(np.sqrt)
    #discretize position
    point_list_x = []
    point_list_y = []
    for y_node in range(int(base_data['ynodes'])):
        for x_node in range(int(base_data['xnodes'])):
            point_list_x.append(x_node)
            point_list_y.append(y_node)
    #calculate angle, that each vector makes with base vectors; for each position
    for related_vec in base_vectors:
        angle = calculate_angle(data, related_vec)
        #increase standard deviation to have more visible effect
        angles.append(angle)
        sensitive = pd.Series(np.power(angle,25))
        sens.append(sensitive)
    counter = 0
    figs = []
    for sen in sens:
        fig = plt.figure()
        fig.suptitle('Direction : Magnetization')
        sp = fig.add_subplot(111)
        cax = sp.scatter(point_list_x, point_list_y, c=tuple(sen), cmap=cm.jet)

        sp.set_title("Color for base vector: "+base_vectors[counter].to_string())
        fig.colorbar(cax)
        figs.append(fig)
        counter += 1
    '''
    below would create a proper subplot
    for i in range(3):
        plt.subplot(3,1,i+1)
        plt.scatter(point_list_x, point_list_y, c=tuple(sens[i]), cmap=cm.jet)
        plt.title("Color for base vector: {}".format(base_vectors[i]))
        plt.colorbar()
    plt.show()
    '''
    counter = 0
    for sen, angle in zip(sens,angles):
        print("Iteration series :{}".format(counter))
        print("Angle, Senes :\n Maximum : {}, {}".format(np.max(angle), np.max(sen)))
        print("Angle, Senes :\n Minumum : {}, {}".format(np.min(angle), np.min(sen)))
        print("Angle: \n Mean : {}, \n Median : {}, \n Std : {}".format(np.mean(angle), np.median(angle), np.std(angle)))
        print("Sens: \n Mean : {}, \n Median : {}, \n Std : {}".format(np.mean(sen), np.median(sen), np.std(sen)))
        counter += 1
    return figs
