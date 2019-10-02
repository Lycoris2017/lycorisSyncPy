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
#cluster = pd.read_csv("claus_file.csv")
#cluster = pd.read_csv("claus_file_new.csv")
cluster = pd.read_csv("Run_20190721_234548.dat.GBL_input.csv")

#cluster =cluster.iloc[:100]

print(cluster.head(3))

x=np.genfromtxt('run400_trigN_mask.csv', dtype= int , names=('trigN'), delimiter = '\n', usecols = (0), unpack=True )
#print (x)

df = pd.DataFrame(x)


res = pd.merge(cluster, df, on = 'trigN')


# print into the telfile.py style
# - line with hit information: planeID, (local) x, y, z
# - last line with event information: run ,event number

#res = res.drop(columns=['Event Number', 'time'])
res = res.drop(columns=['Event Number', 'runtime', 'Significance'])

res['x-pos'] = 0.0
res.rename( columns = {'position': 'y-pos'}, inplace = True)
cols = res.columns.tolist()
cols = cols[:1]+ cols[2:]+ cols[1:2]
res = res[cols]
res['z-pos'] = 0.0

cols = res.columns.tolist()
cols = cols[:1] + cols[-3:] + cols[1:-3]
res=res[cols]
print (res.columns.tolist())
print(res.head(2))

#-- quality check: how many hit clusters for each trigger?
freq = pd.DataFrame( {'count': res.groupby( ['trigN'] ).size()} ).reset_index()
print ("- number of hit clusters for each trigger?\n", freq['count'].unique())

#print (type(res.trigN))
#print(res.info(verbose=True))


print ("Unique trigger Numbers:\n", res.trigN.unique()) # return an array
for i in (res.trigN.unique()):
    if i<10:
        print (res[res.trigN==i].loc[:, res.columns != 'trigN'])
    with open('res.dat', 'a') as f:
        f.write( res[res.trigN==i].loc[:, res.columns != 'trigN'].to_string( header = False, index=False) )
        f.write('\n400 %d 0.0\n'%(i)) # add header line

    #with open('res.csv', 'a') as f:
        #res[res.trigN==i].loc[:, res.columns != 'trigN'].to_csv(f, header = False, index=False) # add hit lines
        #f.write('\n255,%d,0.0\n'%(i)) # add header line
