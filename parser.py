import pandas as pd

filename='test.txt'
skiprows=[x for x in range(39)]
pd.read_csv(filename, skiprows=to_skip)
