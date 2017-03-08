import pandas as pd
import sys

filename='./data/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'

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

base_data, count = extract_base_data(filename)
to_skip=[x for x in range(count)]
a=['Whitespace', 'x','y','z']
data = pd.read_csv(filename, delimiter=' ', skiprows=to_skip)
data.columns = a
data.drop('Whitespace', axis=1, inplace=True)
data.drop([data.shape[0]-2,data.shape[0]-1],axis=0, inplace=True)
print(list(data))
print(data.head())
print(data.tail())
print(data.shape)
print(data.describe())
