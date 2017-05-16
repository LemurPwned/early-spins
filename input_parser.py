import tiny_vectors as vc
import time
from graph_panels import *

def extract_base_data(filename):
    '''
    .omf format reader
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
                    base_data[g[2:x]] += g[x + 1:-1]
                else:
                    base_data[g[2:x]] = g[x + 1:-1]
                try:
                    base_data[g[2:x]] = float(base_data[g[2:x]])
                except:
                    pass
    f.close()
    return base_data, count


def read_header_file(filename):
    '''
    .odt format reader
    '''
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

def process_batch(df, base_data):
    vectors = []
    temp_color = []
    xpos = 0
    ypos = 0
    zpos = 0
    xc = int(base_data['xnodes'])
    yc = int(base_data['ynodes'])
    zc = int(base_data['znodes'])
    xb = float(base_data['xbase']) * 1e9
    yb = float(base_data['ybase']) * 1e9
    zb = float(base_data['zbase']) * 1e9
    xv = df['x'].tolist()
    yv = df['y'].tolist()
    zv = df['z'].tolist()
    for x, y, z in zip(xv,yv,zv):
        xpos += 1
        if xpos >= xc:
            ypos += 1 + (xpos % xc)
            xpos = 0
        if ypos >= yc:
            zpos += 1 + (ypos % yc)
            ypos = 0
            xpos = 0
        xtemp = xpos * xb
        ytemp = ypos * yb
        ztemp = zpos * zb
        c = vc.Vector(x, y, z)
        if np.abs(c.x + c.y + c.z) > 0:
            k = c.norm
            vectors.append([xtemp, ytemp, ztemp, xtemp + (c.x / k),
                            ytemp + (c.y / k), ztemp + (c.z/k)])
            temp_color.append((c.x/k, c.y/k, c.z/k))
        else:
            continue
    return vectors, temp_color

def process_batch_sensitive(df, base_data):
    '''
    increases the displayed sensitivity of data
    '''
    b1 = vc.Vector(1, 0, 0)
    angles = []
    vectors = []
    xpos = 0
    ypos = 0
    zpos = 0
    power = 5
    xc = int(base_data['xnodes'])
    yc = int(base_data['ynodes'])
    xb = float(base_data['xbase']) * 1e9
    yb = float(base_data['ybase']) * 1e9
    zb = float(base_data['zbase']) * 1e9
    #start = time.time()
    for index, row in df.iterrows():
        xpos += 1
        if xpos >= xc:
            ypos += 1 + (xpos % xc)
            xpos = 0
        if ypos >= yc:
            zpos += 1 + (ypos % yc)
            ypos = 0
            xpos = 0

        xtemp = xpos * xb
        ytemp = ypos * yb
        ztemp = zpos * zb
        c = vc.Vector(row[0], row[1], row[2])
        if np.abs(c.x + c.y + c.z) > 0:
            k = c.norm
            vectors.append([xtemp, ytemp, ztemp, xtemp + c.x / k,
                            ytemp + c.y / k, ztemp + c.z / k])
            angle = np.power(vc.relative_direction(c, b1), power)
            angles.append(angle)
        else:
            continue
    series = generate_color_series(len(angles))
    temp_color = [x for (y, x) in sorted(zip(angles, series))]
    #end = time.time()
    #print("TIME : {}\n".format(end - start))
    return angles, vectors, temp_color

if __name__ == "__main__":

    filename = './data/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    filename2 = './data/voltage-spin-diode.odt'
    base_data, count = extract_base_data(filename)
    to_skip = [x for x in range(count)]
    data = form_dataframe(filename, to_skip)

    # set of base vectors
    v1 = vc.Vector(1, 0, 0)
    v2 = vc.Vector(0, 1, 0)
    v3 = vc.Vector(0, 0, 1)

    # split layers
    layers = layer_splitter(data, base_data)

    figs = color2d(layers[4], [v1, v2, v3], base_data)
    # callback_plotter(figs)

    df = read_header_file(filename2)
    graph = plotters(df, ('Iteration', 'Total energy'), ('step', 'J'))
    callback_plotter(graph)
    #anglify

    #data.loc[~(data == 0).all(axis=1)] = np.nan
    #sdf = data.to_sparse()
    #print(sdf.density)
    #print(base_data)
