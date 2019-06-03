import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import argparse

kpix_name = 'runtime_full_ns'
tlu_name = 'timestamp_64' #'timestamp_low'
mask_file = 'run255_trigN_mask.csv'
####
#kpix = pd.read_csv("dumpkpix_trigger.csv")
kpix = pd.read_csv("Run_20190505_111442.csv")
#tlu = pd.read_csv("run255_trigger.csv")
tlu = pd.read_csv("run255_ts64.csv")


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
print (" Debug -- kpix has ", kpix.index, ",  tlu has ", tlu.index)

diffs = tskpix - tstlu

print( np.where(diffs<0))  # get index
print (tskpix[2648:2655])
print (tstlu[2648:2655])
#print (diffs[5407:5409])
#print (diffs[8032:8033])


# NEW! produce a trigN mask file by comparing KPiX to TLU timestamp:
trign = np.array(tlu.trigger)
trign = np.delete(trign, np.where(diffs<0))
print(' write to ', mask_file)
np.savetxt(mask_file, trign, delimiter='\n', fmt='%d')

exit()
diffs = np.delete(diffs, np.where(diffs<0))                   

xmin = np.amin(diffs)-10
xmax = np.amax(diffs)+10
if (xmax-xmin)%5!=0 or xmin < 0 or xmax > 2**32:
    print("ERROR: check your data! nbins = %.2f, xmin, xmax = %.2f, %.2f"% ((xmax-xmin)/5, xmin+10, xmax-10) )
    exit()
nbins = int((xmax-xmin)/5)
print("nbins = ", nbins, "; xmin, xmax = ", xmin+10, xmax-10)

n, bins, patches = plt.hist(diffs, nbins, range=(xmin,xmax), density=False, facecolor='g', alpha=0.75)

plt.xlabel('Timestamp [ns]')
plt.ylabel('Ab.')
plt.title('Histogram')
#plt.grid(True)
plt.show()
