import pandas as pd
import sys
import numpy as np
import tiny_vectors as vc


filename='./data/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
filename2='./data/voltage-spin-diode.odt'
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

def read_that_badass_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    f.close()
    lines = [x.strip() for x in lines]
    print(len(lines))
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

def calculate_color(data, relate):
    norms = pd.Series(data['x']**2+data['y']**2+data['z']**2, dtype=np.float).apply(np.sqrt)
    dot = pd.Series(data['x']*relate.x+data['y']*relate.y+data['z']*relate.z, dtype=np.float)
    angle = pd.Series(dot/(relate.norm*norms), dtype=np.float).apply(np.arccos).fillna(np.float(-1))
    color = pd.Series(angle, dtype=tuple).apply(vc.color_map)
    return color

base_data, count = extract_base_data(filename)
to_skip=[x for x in range(count)]
data = form_dataframe(filename, to_skip)
print(base_data)
relate = vc.Vector(1,0,0)
color = calculate_color(data, relate)

row = next(data.iterrows())[1]
print(row[2])
print(data.shape[0])

df = read_that_badass_file(filename2)
#print(df.head())
