import pandas as pd
import numpy as np
from graph_panels import *

def extract_base_data(filename):
    '''
    returns dictionary with headers and their corresponding values
    and number of these headers
    '''
    base_data = {}
    count = 0
    with open(filename, 'r') as f:
        g = f.readline()
        while g.startswith('#'):
            count += 1
            g = f.readline()
            if ':' in g:
                x = g.index(':')
                if g[2:x] in base_data:
                    base_data[g[2:x]] += g[x+1:-1]
                else:
                    base_data[g[2:x]] = g[x+1:-1]
                try:
                    #print(float(base_data[g[2:x]]))
                    base_data[g[2:x]] = float(base_data[g[2:x]])
                except:
                    pass
    f.close()
    return base_data, count

def read_header_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    f.close()
    lines = [x.strip() for x in lines]
    print("{} lines have been read ".format(len(lines)))
    lines = [x.split(' ') for x in lines]
    new_cont = []
    lines = lines[5:-1]
    for line in lines:
        temp_line = []
        for el in line:
            try:
                new_el = float(el)
                temp_line.append(new_el)
            except:
                pass
        new_cont.append(temp_line)
    col = ['Total energy', 'Energy calc count', 'Max dm/dt', 'dE/dt',
        'Delta E', '_MRmagnetoresistance', 'Energy ', 'Max Spin Ang',
        'Stage Max Spin Ang', 'Run Max Spin Ang', '_DemagEnergy',
        '_MREnergy', '_TwoSurfaceExchangeFFEnergy',
        '_UniaxialAnisotropystatEnergy', '_UniaxialAnisotropyipEnergy ',
        '_UniaxialAnisotropydynEnergy', '_UZeemanEnergy', '_UZeemanB',
        '_UZeemanBx', '_UZeemanBy', '_UZeemanBz', 'Iteration', 'Stage iteration',
        'Stage ', 'mx', 'my', 'mz', 'Last time step', 'Simulation time']

    df = pd.DataFrame.from_records(new_cont, columns=col)
    return df

def form_dataframe(filename, to_skip, cols=['Whitespace', 'x','y','z']):
    data = pd.read_csv(filename, delimiter=' ', skiprows=to_skip)
    if cols != None:
        data.columns = cols
        data.drop('Whitespace', axis=1, inplace=True)
        data.drop([data.shape[0]-2,data.shape[0]-1],axis=0, inplace=True)
        data[['x','y','z']] = data[['x','y','z']].astype(float)
    return data

if __name__=="__main__":
    filename = './data/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    filename2 = './data/voltage-spin-diode.odt'
    base_data, count = extract_base_data(filename)
    print(base_data, count)
    to_skip=[x for x in range(count)]
    data = form_dataframe(filename, to_skip)
    #set of base vectors
    v1 = vc.Vector(1,0,0)
    v2 = vc.Vector(0,1,0)
    v3 = vc.Vector(0,0,1)

    layers = layer_splitter(data, base_data)

    figs = color2d(layers[4], [v1, v2, v3], base_data)
    #callback_plotter(figs)

    df = read_header_file(filename2)
    graph = plotters(df, ('Iteration', 'Total energy'), ('step','J'))
