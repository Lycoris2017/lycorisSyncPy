# Mengqing @ 2019-May-31
# temperary python code to provide sync data of TLU + kpix
# final data strategy:1) refactory the code to c++ with analysis framework; 2) online merging on EUDAQ2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import argparse

from collections import defaultdict #non-sorted
acc_delay = [105.0, 130.0]


parser = argparse.ArgumentParser()
parser.add_argument("run", help="run number you have to give")
parser.add_argument("-i", "--input", default = "Run_20190721_234548.dat.GBL_input.csv",
                    help="list of lycoris clusters with all numerical features in csv")
parser.add_argument("-m", "--mask", default = "matched_trigN_mask.csv",
                    help="a list of good trig IDs produced from explorer.py ")
args = parser.parse_args()
print(f" input file: {args.input}")


####
#cluster = pd.read_csv("claus_file.csv")
#cluster = pd.read_csv("claus_file_new.csv")
cluster = pd.read_csv(args.input)

## debug/test: ONLY check first 100 triggers
#cluster = cluster.loc[cluster['trigN'] <= cluster['trigN'].min()+100 ]
 
print(" Check raw cluster dataframe:\n", cluster.head(3))

x=np.genfromtxt(args.mask, dtype= int , names=('trigN'), delimiter = '\n', usecols = (0), unpack=True )
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

print(" Check result columns:\n",res.columns.tolist())
print(" Show first two rows of res with header:\n", res.head(2))

#-- Simply Analysis for Quality check: 
freq = pd.DataFrame( {'count': res.groupby( ['trigN'] ).size()} ).reset_index()
print (f"- range of number of hit clusters for each trigger? from {freq['count'].unique().min()} to {freq['count'].unique().max()}.\n")
print (f"- range of hit cluster size? from {res['Size'].min()} to {res['Size'].max()}.\n")
print ("- frequency of different sized cluster? ")
freq = pd.DataFrame( {'freq_%': 100*res.groupby( ['Size'] ).size()/res.shape[0] } ).reset_index()
print ( freq.loc[ freq['Size']<=res['Size'].max() ] )
print ("\n- Plot all raw cluster charge out...")

mad = res['Charge'].mad()
median = res['Charge'].median()
print(f" median is {median:.2f}, mad is {mad:.2f}")

fig, axs = plt.subplots(2, 3, figsize=(16,10))
#sns.boxplot(x=res['Charge'], ax=axs[0,0])

cut = (res['Charge']<10) & (res['Significance2']>7.)
layer0=res['Layer']==13
layer1=res['Layer']==14
layer2=res['Layer']==15

sns.distplot(res['Charge'].loc[cut&layer0], bins = 200, ax = axs[0][0], kde=False)
sns.distplot(res['Charge'].loc[cut&layer1], bins = 200, ax = axs[0][1], kde=False)
sns.distplot(res['Charge'].loc[cut&layer2], bins = 200, ax = axs[0][2], kde=False)
#sns.set()
#print(res['y-pos'].loc[cut&layer0]/1000)
sns.distplot(res['y-pos'].loc[cut&layer0]/1000, bins = 200, ax = axs[1][0], kde=False)
sns.distplot(res['y-pos'].loc[cut&layer1]/1000, bins = 200, ax = axs[1][1], kde=False)
sns.distplot(res['y-pos'].loc[cut&layer2]/1000, bins = 200, ax = axs[1][2], kde=False)

axs[0][0].set(xlabel="Charge [fC]", ylabel="Cluster", title="layer 0")
axs[0][1].set(xlabel="Charge [fC]", ylabel="Cluster", title="layer 1")
axs[0][2].set(xlabel="Charge [fC]", ylabel="Cluster", title="layer 2")
axs[1][0].set(xlabel="y [um]", ylabel="Cluster", title="layer 0")
axs[1][1].set(xlabel="y [um]", ylabel="Cluster", title="layer 1")
axs[1][2].set(xlabel="y [um]", ylabel="Cluster", title="layer 2")

plt.show()

#print(res.info(verbose=True))
f = open(f'res_{args.run}.dat', 'w')
#print ("Unique trigger Numbers:\n", res.trigN.unique()) # return an array
for i in (res.trigN.unique()):
    if i<10:
        print (res[res.trigN==i].loc[:, res.columns != 'trigN'])
    #with open('res.dat', 'a') as f:
    f.write( res[res.trigN==i].loc[:, res.columns != 'trigN'].to_string( header = False, index=False) )
    f.write('\n%s %d 0.0\n'%(args.run,i)) # add header line
