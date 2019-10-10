#!/usr/bin/python3

"""
 Mengqing @ 2019-10-10 <mengqing.wu@desy.de>
 
 Python code to combine kpix cluster event file MimosaTLU event by matching Timestamp 

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tlu", default = "test_tlu.csv",
                    help="tlu timestamps file .csv")
parser.add_argument("-k", "--kpix", default = "test_cluster.csv",
                    help="kpix cluster file with trigger timestamps .csv")
args = parser.parse_args()
print(f" tlu file: {args.tlu}, kpix file: {args.kpix}")
kpix = pd.read_csv(args.kpix)
tlu = pd.read_csv(args.tlu)

## lighter your dataframes
kmask=["Event Number","runtime_ns"]
tmask=["trigger","timestamp_low"]
tts="timestamp_low"
kts="runtime_ns"
kpix=kpix[kmask]
tlu =tlu[tmask]

kpix=kpix.drop_duplicates()

kk = kpix.shape[0]
tt = tlu.shape[0]
print(f"kpix has {kk} entries, tlu has {tt} entries")
#longer = kpix if kk>tt else tlu
#shorter = kpix if kk<tt else tlu
print("Lycoris trig ts at 0 is:", kpix.iloc[0][kts])
print("Tlu+Mi  trig ts at 0 is:",tlu.iloc[0][tts])
## In the common clock sync, the 0 trigger should be same from tlu to lycoris
## the 1st trigger from the combined TLUMimosa can be not the 0, but
kpix0= kpix.iloc[0][kts]
tlu0 =  tlu.iloc[0][tts]

diff = kpix0 - tlu0
ikk = 0
print(diff)
## If Kpix starts earlier than TLU+mimosa:
while True:
    kpixi=kpix.iloc[ikk][kts]
    diff = kpixi - tlu0
    if diff>0 or ikk>=kk-1:
        break
    else:
        ikk+=1

kpix = kpix.iloc[ikk:]
print(kpix)
"""
1) do a loop to get time delay, outer loop over kpix, inner is tlu
"""
diffs = [] 
outliers = []
## loop over kpix
diff = 0
limit=1000 # only allow diff within 1000ns
itt=0
"""
The following conditions are taken into account:
1) missing value of TLU or KPiX side
2) glitches of KPiX TIMESTAMP: some ts suddenly becomes very small
"""
for kpixi in kpix[kts]:
    print(kpixi)
    while True:
        if itt>=tt-1:
            break;
        tlui = tlu.iloc[itt][tts]
        diff = kpixi-tlui
        if diff<0:
            break
        if diff>0:
            if diff< limit:
                #print (kpixi, tlui, diff)
                diffs.append(diff)
                break
            else:
                itt+=1
# Plot
diffs = np.array(diffs)
xmin = np.amin(diffs)-10
xmax = np.amax(diffs)+10
nbins = int(round((xmax-xmin)/5))

n, bins, patches = plt.hist(diffs, nbins, range=(xmin,xmax), density=False, facecolor='g', alpha=0.75)
plt.xlabel('Timestamp [ns]')
plt.ylabel('Ab.')
plt.title('Histogram')
#plt.grid(True)
plt.show()

"""
2) do a match
"""
