import pandas as pd
import numpy as np
import tiny_vectors as vc
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
                    base_data[g[2:x]] += g[x + 1:-1]
                else:
                    base_data[g[2:x]] = g[x + 1:-1]
                try:
                    # print(float(base_data[g[2:x]]))
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


def form_dataframe(filename, to_skip, cols=['Whitespace', 'x', 'y', 'z']):
    data = pd.read_csv(filename, delimiter=' ', skiprows=to_skip)
    if cols != None:
        data.columns = cols
        data.drop('Whitespace', axis=1, inplace=True)
        data.drop([data.shape[0] - 2, data.shape[0] - 1], axis=0, inplace=True)
        data[['x', 'y', 'z']] = data[['x', 'y', 'z']].astype(float)
    return data


def calculate_color(data, relate):
    '''
    calculates the color of each vector
    '''
    norms = pd.Series(data['x'] ** 2 + data['y'] ** 2 + data['z'] ** 2, dtype=np.float).apply(np.sqrt)
    dot = pd.Series(data['x'] * relate.x + data['y'] * relate.y + data['z'] * relate.z, dtype=np.float)
    angle = pd.Series(dot / (relate.norm * norms), dtype=np.float).apply(np.arccos).fillna(np.float(-1))
    color = pd.Series(angle, dtype=tuple).apply(vc.color_map)
    return color


def layer_splitter(data, base_data):
    '''
    splits data into n separate layers with proper indices
    '''
    (x, y, z) = (int(base_data['xnodes']), int(base_data['ynodes']), int(base_data['znodes']))
    thickness = x * y
    layers = [data.iloc[thickness * i:thickness * i + thickness, :] for i in range(z)]
    return layers


def plotters(data):
    cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
    # sns.kdeplot(data['Total energy'], cut=0, bw=0.2);
    sns.jointplot(data['mx'], data['Total energy'], kind="kde")
    plt.show()


def color2d(data, base_vectors):
    '''
    this function maps layer and shows 2d plot for that layer
    '''
    angles = []
    sens = []
    norms = pd.Series(data['x'] ** 2 + data['y'] ** 2 + data['z'] ** 2, dtype=np.float).apply(np.sqrt)
    for related_vec in base_vectors:
        dot = pd.Series(data['x'] * related_vec.x + data['y'] * related_vec.y + data['z'] * related_vec.z,
                        dtype=np.float)
        angle = pd.Series(dot / (related_vec.norm * norms), dtype=np.float).apply(np.arccos).fillna(np.float(0))
        angles.append(angle)
        sensitive = pd.Series(np.power(angle, 25))
        sens.append(sensitive)
    # sns.jointplot(data['x'], data['y'], hue=angles[0], kind="hex")
    plt.scatter(data['x'], data['y'], c=sens[0], cmap=cm.jet)
    plt.show()
    print(np.max(angles[0]), np.max(sens[0]))
    print(np.min(angles[0]), np.min(sens[0]))
    print(np.mean(angles[0]), np.median(angles[0]), np.std(angles[0]))
    print(np.mean(sens[0]), np.median(sens[0]), np.std(sens[0]))


if __name__ == "__main__":
    filename = './data/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    filename2 = './data/voltage-spin-diode.odt'
    base_data, count = extract_base_data(filename)
    print(base_data, count)
    to_skip = [x for x in range(count)]
    data = form_dataframe(filename, to_skip)
    print(data)