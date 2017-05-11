if __name__ == "__main__":
    from tiny_vectors import *
    from graph_panels import *
    filename = './data/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    filename2 = './data/voltage-spin-diode.odt'
    base_data, count = extract_base_data(filename)
    to_skip = [x for x in range(count)]
    data = form_dataframe(filename, to_skip)

    # set of base vectors
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    v3 = Vector(0, 0, 1)

    # split layers
    layers = layer_splitter(data, base_data)

    figs = color2d(layers[4], [v1, v2, v3], base_data)
    # callback_plotter(figs)

    df = read_header_file(filename2)
    graph = plotters(df, ('Iteration', 'Total energy'), ('step', 'J'))
else:
    try:
        from tiny_vectors import *
        from graph_panels import *
    except:
        from CPU3D.tiny_vectors import *
        from CPU3D.graph_panels import *

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
    start = time.time()
    for index, row in df.iterrows():
        if xpos >= xc:
            ypos += 1 + (xpos % xc)
            xpos = 0
        if ypos >= yc:
            zpos += 1 + (ypos % yc)
            ypos = 0
            xpos = 0
        xpos += 1
        xtemp = xpos * xb
        ytemp = ypos * yb
        ztemp = zpos * zb

        c = vc.Vector(row[0], row[1], row[2])
        if np.abs(row[0] + row[1] + row[2]) > 0:
            vectors.append([xtemp, ytemp, ztemp, xtemp + row[0] / c.norm,
                            ytemp + row[1] / c.norm, ztemp + row[2] / c.norm])
            angles.append(np.power(vc.relative_direction(c, b1), power))
        else:
            continue

    max_angle = np.max(angles)
    series = generate_color_series(len(angles))
    temp_color = [x for (y, x) in sorted(zip(angles, series))]
    end = time.time()
    #print("TIME : {}\n".format(end - start))
    return angles, vectors, temp_color


def topology(base_data):
    xpos = 0
    ypos = 0
    zpos = 0
    vectors_init = []
    iterations = base_data['xnodes']*base_data['ynodes']*base_data['znodes']
    for i in range(iterations):
        if xpos >= int(base_data['xnodes']):
            ypos += 1 + (xpos % int(base_data['xnodes']))
            xpos = 0
        if ypos >= int(base_data['ynodes']):
            zpos += 1 + (ypos % int(base_data['ynodes']))
            ypos = 0
            xpos = 0
        xpos += 1
        xtemp = xpos * float(base_data['xbase']) * 1e9
        ytemp = ypos * float(base_data['ybase']) * 1e9
        ztemp = zpos * float(base_data['zbase']) * 1e9
        vectors_init.append([xtemp, ytemp, ztemp, xtemp])
    return vectors_init

def form_layer_structure(df, base_data):
    xpos = 0
    ypos = 0
    zpos = 0
    b1 = vc.Vector(1, 0, 0)
    norm = (np.square(df['x']) + np.square(df['y']) + np.square(df['z'])).apply(np.sqrt)
    _angles = df['x']*b1.x + df['y']*b1.y + df['z']*b1.z
    _angles = (((_angles/norm).apply(np.arccos)**25)/np.max(_angles)).fillna(0)
    df['norm'] = norm
    df['angles'] = _angles
    vectors = []
    angles = []
    colors = []
    for index, row in df.iterrows():
        if xpos >= int(base_data['xnodes']):
            ypos += 1 + (xpos % int(base_data['xnodes']))
            xpos = 0
        if ypos >= int(base_data['ynodes']):
            zpos += 1 + (ypos % int(base_data['ynodes']))
            ypos = 0
            xpos = 0
        xpos += 1
        xtemp = xpos * float(base_data['xbase']) * 1e9
        ytemp = ypos * float(base_data['ybase']) * 1e9
        ztemp = zpos * float(base_data['zbase']) * 1e9
        if row[3] > 0:
            vectors.append([xtemp, ytemp, ztemp, xtemp + row[0] / row[3],
                            ytemp + row[1] / row[3], ztemp + row[2] / row[3]])
            angles.append(row[4])
        else:
            continue

        series = generate_color_series(len(angles))
        colors = [x for (y, x) in sorted(zip(angles, series))]

    return vectors, angles, colors

def histeresis(angle):
    low = np.percentile(angle[angle > 0], 66, interpolation='higher')
    high = np.percentile(angle[angle > 0], 33, interpolation='lower')
    return low, high


def colorify(dataframe, low, high):
    dataframe['color'] = np.zeros(dataframe.shape[0])
    dataframe['color'][(dataframe['angles'] > low) & (dataframe['angles'] < high) & (dataframe['angles'] > 0)] = 1
    dataframe['color'][(dataframe['angles'] > high) & (dataframe['angles'] > 0)] = 2
    dataframe['color'][(dataframe['angles'] < low) & (dataframe['angles'] > 0)] = 3
    return dataframe

