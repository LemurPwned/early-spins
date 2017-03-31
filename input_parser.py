import pandas as pd
import numpy as np
import tiny_vectors as vc
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm

def extract_base_data(filename):
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

def calculate_angle(data, relate):
    '''
    calculates the color of each vector
    '''
    norms = pd.Series(data['x']**2+data['y']**2+data['z']**2, dtype=np.float).apply(np.sqrt)
    dot = pd.Series(data['x']*relate.x+data['y']*relate.y+data['z']*relate.z, dtype=np.float)
    angle = pd.Series(dot/(relate.norm*norms), dtype=np.float).apply(np.arccos).fillna(np.float(-1))
    return angle


def layer_splitter(data, base_data):
    '''
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

def plotters(data):
    cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
    #sns.kdeplot(data['Total energy'], cut=0, bw=0.2);
    sns.jointplot(data['mx'],data['Total energy'], kind="kde")
    plt.show()

def color2d(data, base_vectors, base_data):
    '''
    this function maps layer and shows 2d plot for that layer
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

    for angle in sens:
        plt.scatter(point_list_x, point_list_y, c=tuple(angle), cmap=cm.jet)
        plt.show()
    print("Angle, Senes :\n Maximum : {}, {}".format(np.max(angles[0]), np.max(sens[0])))
    print("Angle, Senes :\n Minumum : {}, {}".format(np.min(angles[0]), np.min(sens[0])))
    print("Angle: \n Mean : {}, \n Median : {}, \n Std : {}".format(np.mean(angles[0]), np.median(angles[0]), np.std(angles[0])))
    print("Sens: \n Mean : {}, \n Median : {}, \n Std : {}".format(np.mean(sens[0]), np.median(sens[0]), np.std(sens[0])))


if __name__=="__main__":
    filename = './data/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    filename2 = './data/voltage-spin-diode.odt'
    base_data, count = extract_base_data(filename)
    to_skip=[x for x in range(count)]
    data = form_dataframe(filename, to_skip)
    #print(base_data)

    relate = vc.Vector(1,0,0)
    #print(base_data)

    v1 = vc.Vector(1,0,0)
    v2 = vc.Vector(0,1,0)
    v3 = vc.Vector(0,0,1)

    layers = layer_splitter(data, base_data)

    color2d(layers[4], [v1, v2, v3], base_data)
    data[['x','y','z']] = data[['x','y','z']]/np.max(np.abs(data[['x','y','z']]))
    print(np.max(np.abs(data)))
    #print(data.columns.values.tolist())
    #print(data.shape[0])

    df = read_header_file(filename2)
    #print(df.columns.values.tolist(), df.shape)
    #print(df['Iteration'].head())
    #plotters(df)
