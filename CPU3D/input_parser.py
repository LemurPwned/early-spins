import time
from CPU3D.tiny_vectors import *
from CPU3D.graph_panels import *
import struct


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

def fortran_list(filename):
    vectors = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    f.close()
    vectors = [g.strip().split(' ') for g in lines if '#' not in g]
    vectors = [[float(row[0]), float(row[1]), float(row[2])] for row in vectors]
    return np.array(vectors)

def process_fortran_list(fortran_list, base_data):
    xc = int(base_data['xnodes'])
    yc = int(base_data['ynodes'])
    zc = int(base_data['znodes'])
    xb = float(base_data['xbase']) * 1e9
    yb = float(base_data['ybase']) * 1e9
    zb = float(base_data['zbase']) * 1e9
    #fortran_list = np.apply_along_axis(np.linalg.norm, 1, fortran_list)
    fortran_list = np.array([x*100/np.linalg.norm(x)
        for x in np.nditer(fortran_list, flags=['external_loop'])]).reshape(35*35*5,3)
    vectors = [[xb * x%xc, yb * y%yc, zb * z%zc,
                xb * x%xc, yb * y%yc, zb * z%zc]
                for z in range(zc) for y in range(yc) for x in range(xc)]
    return vectors, fortran_list

def listy(fortran_list):
        #temp_color = [(x[0]/np.sqrt(x[0]**2 + x[1]**2 + x[2]**2),x[2]/np.sqrt(x[0]**2 + x[1]**2 + x[2]**2),
        #               x[1]/np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)) for z in fortran_list for y in z for x in y
        #               if np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)]
    for z in fortran_list:
        for y in z:
            for x in y:
                xtemp = xb * xp
                ytemp = yb * yp
                ztemp = zb * zp
                k = np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)
                if k>0:
                    c+=1
                    vectors.append([xtemp, ytemp, ztemp, xtemp + (x[0] / k),
                                   ytemp + (x[1] / k), ztemp + (x[2] / k)])
                    temp_color.append((x[0]/k, x[1]/k, x[2]/k))
                xp += 1
            yp += 1
            xp = 0
        zp += 1
        yp = 0
    return vectors, temp_color

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
    c = 1
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
        k = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        if k > 0:
            c+=1
            vectors.append([xtemp, ytemp, ztemp, xtemp + (x / k),
                            ytemp + (y / k), ztemp + (z / k)])
            temp_color.append((x/k, y/k, z/k))
    return vectors, temp_color

def process_batch_sensitive(df, base_data):
    '''
    increases the displayed sensitivity of data
    '''
    b1 = Vector(1, 0, 0)
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
        c =  Vector(row[0], row[1], row[2])
        if np.abs(c.x + c.y + c.z) > 0:
            k = c.norm
            vectors.append([xtemp, ytemp, ztemp, xtemp + c.x / k,
                            ytemp + c.y / k, ztemp + c.z / k])
            angle = np.power(relative_direction(c, b1), power)
            angles.append(angle)
        else:
            continue
    series = generate_color_series(len(angles))
    temp_color = [x for (y, x) in sorted(zip(angles, series))]
    return vectors, temp_color

def process_header(headers):
    base_data = {}
    headers = headers.replace('\'', "")
    headers = headers.replace(' ', "")
    headers = headers.replace('\\n', "")
    headers = headers.split('#')
    for header in headers:
        if ':' in header:
            components = header.split(':')
            try:
                base_data[components[0]] = float(components[1])
            except:
                base_data[components[0]] = components[1]
    return base_data

def odt_reader(filename):
    header_lines = 4
    header = []
    i = 0
    with open(filename, 'r') as f:
        while i < header_lines:
            lines = f.readline()
            header.append(lines)
            i += 1
        units = f.readline()
        lines = f.readlines()
    f.close()
    cols = header[-1]
    cols = cols.replace("} ", "")
    cols = cols.replace("{", "")
    cols = cols.split("Oxs_")
    del cols[0]
    cols = [x.strip() for x in cols]

    units = units.split(" ")
    units
    units = [x.strip() for x in units]

    dataset = []
    lines = [x.strip() for x in lines]
    print("{} lines have been read ".format(len(lines)))
    lines = [x.split(' ') for x in lines]
    for line in lines:
        temp_line = []
        for el in line:
            try:
                new_el = float(el)
                temp_line.append(new_el)
            except:
                pass
        dataset.append(temp_line)
    dataset = dataset[:-1]
    df = pd.DataFrame.from_records(dataset, columns=cols)
    iterations = len(lines) -1
    return df, iterations

def binary_read(filename, cols = ['x', 'y', 'z']):
    lists = []
    a_tuple = []
    c = 0
    base_data = {}
    validity = False
    iterator = -10
    validation = 123456789012345.0 #this is IEEE validation value
    with open(filename, 'rb') as f:
        while validity == False and iterator < 50:
            headers = f.read(24*38 + iterator) #idk xD
            #print("Header \n",headers)
            headers = str(headers)
            check_value = struct.unpack('d', f.read(8))[0]
            #print(base_data)
            #print("Check value for 8-binary {}".format(check_value))
            if check_value == validation:
                #print("Proper reading commences ...")
                #print("Detected value for 8-binary {}".format(check_value))

                validity = True
                break
            else:
                #print("Validity check failed")
                #print("Adjusting binary size read")
                f.seek(0)
                iterator += 1
        if iterator == 24  : raise TypeError
        base_data = process_header(headers)
        #print(headers)
        #print(base_data)
        b = f.read(8)
        #TODO quantize below
        k = 3*base_data['xnodes']*base_data['ynodes']*base_data['znodes'] -1
        counter = 0
        while b and counter < k:
            try:
                p = struct.unpack('d', b)[0]
                c += 1
                counter += 1
                if c%3 == 0:
                    a_tuple.append(p)
                    lists.append(tuple(a_tuple))
                    a_tuple = []
                    c = 0
                else:
                    a_tuple.append(p)
            except struct.error:
                print(b)
                pass
            b = f.read(8)
        b = f.read(36 + 8) #pro debug process
        #print("last line {}".format(b))
    f.close()
    df = pd.DataFrame.from_records(lists, columns=cols)
    return base_data, df
