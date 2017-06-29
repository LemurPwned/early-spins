import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from matplotlib import cm
from CPU3D.input_parser import *
from CPU3D.graph_panels import calculate_angle, populate_list, increase_variance
from CPU3D.tiny_vectors import *


def update_batch_plot(i, data, scat):
    scat.set_array(pd.np.array(data[i], dtype=float))
    return scat


def init_anim(data, title, frame_number, xnodes, ynodes):

    color_data = data
    point_list_x, point_list_y = populate_list(xnodes, ynodes)
    fig = plt.figure()
    c = data[0]
    scat = plt.scatter(point_list_x, point_list_y, c=tuple(c), cmap=cm.jet)
    fig.suptitle(title)
    fig.colorbar(scat)
    ani = animation.FuncAnimation(fig, update_batch_plot,
                                  frames=range(frame_number),
                                  fargs=(color_data, scat))
    plt.show()


def process_batch(filename):
    base_data, count = extract_base_data(filename)
    to_skip = [x for x in range(count)]
    df = form_dataframe(filename, to_skip)
    # split layers
    layers = layer_splitter(df, base_data)

    relate = Vector(1, 0, 0)
    # testing, just one layer for now
    layer = calculate_angle(layers[0], relate)
    layer = increase_variance(layer, 25)
    return layer

def batch_load(directory, iterations, function):
    '''
    iterates over directory and populates the list to sort
    below: deprecated use for now
    iterates over files in directory and performs a function on each ".omf" file
    '''
    handling_list = []
    for filename in os.listdir(directory):
        if iterations <= 0:
            break
        if filename.endswith(".omf"):
            # d.handler = function(directory+'/'+filename)
            handler = directory + '/' + filename
            handling_list.append(handler)
            iterations -= 1
        else:
            continue
    handling_list.sort()
    return handling_list

if __name__ == "__main__":

    N = 100
    file_list = batch_load('../data', N, process_batch)
    batches_to_animate = []
    for filename in file_list:
        batches_to_animate.append(process_batch(filename))
    print(len(batches_to_animate))
    init_anim(batches_to_animate, 'Magnetization direction', N, 35, 35)
