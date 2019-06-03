# Mengqing @ 2019-May-31
# temperary python code to provide sync data of TLU + kpix
# final data strategy:1) refactory the code to c++ with analysis framework; 2) online merging on EUDAQ2
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import argparse

from collections import defaultdict #non-sorted

acc_delay = [105.0, 130.0]
####
cluster = pd.read_csv("claus_file.csv")

#cluster =cluster.iloc[:100]

#print(cluster.head())

x=np.genfromtxt('run255_trigN_mask.csv', dtype= int , names=('trigN'), delimiter = '\n', usecols = (0), unpack=True )
#print (x)

df = pd.DataFrame(x)


res = pd.merge(cluster, df, on = 'trigN')


# print into the telfile.py style
# - line with hit information: planeID, (local) x, y, z
# - last line with event information: run ,event number

res = res.drop(columns=['Event Number', 'time'])

res['x-pos'] = 0.0
#res.columns = ['Sensor', 'x-pos', 'position', 'z-pos', 'trigN']
res.rename( columns = {'position': 'y-pos'}, inplace = True)
cols = res.columns.tolist()
cols = cols[:1]+ cols[2:]+ cols[1:2]
res = res[cols]
res['z-pos'] = 0.0

print (res.columns.tolist())
print(res.head(2))

#-- quality check: how many hit clusters for each trigger?
freq = pd.DataFrame( {'count': res.groupby( ['trigN'] ).size()} ).reset_index()
print (freq['count'].unique())

#print (type(res.trigN))

print (res.trigN.unique()) # return an array
for i in (res.trigN.unique()):
    if i<10:
        print (res[res.trigN==i].loc[:, res.columns != 'trigN'])
    with open('res.csv', 'a') as f:
        res[res.trigN==i].loc[:, res.columns != 'trigN'].to_csv(f,header = False, index=False) # add hit lines
        f.write('255,%d,0.0\n'%(i)) # add header line
