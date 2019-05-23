import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import argparse

kpix_name = 'runtime_full_ns'
tlu_name = 'timestamp_64' #'timestamp_low'
####
#kpix = pd.read_csv("dumpkpix_trigger.csv")
kpix = pd.read_csv("Run_20190505_111442.csv")
#tlu = pd.read_csv("run255_trigger.csv")
tlu = pd.read_csv("run255_ts64.csv")

#print(kpix)

#print(kpix.head())
#print(kpix.info())
#print(tlu.head())
print (' Kpix recorded %i Triggers, while tlu recorded %i Triggers' % (len(kpix.index), len(tlu.index)))

kk = len(kpix.index)
tt = len(tlu.index)
trigs = kk if kk<tt else tt
#trigs = 150

kpix = kpix.iloc[0:trigs]
tskpix = np.array(kpix[kpix_name])

tlu = tlu.iloc[0:trigs]
tstlu = np.array(tlu[tlu_name])
#print (tstlu)
#tlu['timestamp_low'].plot(kind='hist', bins=10)
#plt.xlabel('timestamp [ns]')
#plt.show()


diffs = tskpix - tstlu
print(diffs[:200])

xmin = np.amin(diffs)-10
xmax = np.amax(diffs)+10
if (xmax-xmin)%5!=0:
    print("ERROR: check your data! nbins = ", (xmax-xmin)/5)
    exit()
nbins = int((xmax-xmin)/5)
print("nbins = ", nbins, "; xmin, xmax = ", xmin, xmax)

n, bins, patches = plt.hist(diffs, nbins, range=(xmin,xmax), density=False, facecolor='g', alpha=0.75)

plt.xlabel('Timestamp [ns]')
plt.ylabel('Ab.')
plt.title('Histogram')
#plt.grid(True)
plt.show()
