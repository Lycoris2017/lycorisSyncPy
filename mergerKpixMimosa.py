#!/usr/bin/python3

"""
 Mengqing @ 2019-10-10 <mengqing.wu@desy.de>
 
 Python code to combine kpix cluster event file MimosaTLU event by matching Timestamp 

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import click
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tlu", default = "test_tlu.csv",
                    help="tlu timestamps file .csv")
parser.add_argument("-k", "--kpix", default = "test_cluster.csv",
                    help="kpix cluster file with trigger timestamps .csv")
parser.add_argument("-b", "--bfield", default = 0.0,
                    help="B-field if there is any applicable, [default = 0.0]")

args = parser.parse_args()
print(f" Open files: {args.tlu} for tlu, {args.kpix} for Kpix.")
print(f" B field is set to: {args.bfield}")

_kpix = pd.read_csv(args.kpix)
_tlu = pd.read_csv(args.tlu)

if _tlu['run'].unique().size > 1:
    exit("Your TLU input file is not valid for: [too many run numbers].")
else :
    runnumber = _tlu.iloc[0]['run']



## lighter your dataframes
kmask=["Event Number","runtime_ns"]
tmask=["trigger","timestamp_low"]
tts="timestamp_low"
kts="runtime_ns"
kpix = _kpix[kmask].copy()
tlu  = _tlu[tmask].copy()

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

## If Kpix starts earlier than TLU+mimosa:
while True:
    kpixi=kpix.iloc[ikk][kts]
    diff = kpixi - tlu0
    if diff>0 or ikk>=kk-1:
        break
    else:
        ikk+=1

kpix = kpix.iloc[ikk:]
#print(kpix)
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
with click.progressbar(iterable = range(kk),
                       show_pos=True,
                       label=click.style("Processing", fg="green") )as bar:
    barcount=0
    for kpixi in kpix[kts]:
        #print(kpixi)
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
        #end of while
        bar.update(1)

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
#plt.show()

"""
2) do a match
"""
#print (kpix)
#print (tlu)
# should apply to original _kpix and _tlu
print (" Delta_T =", np.unique(diffs))

maskt = ["event","trigger","ni_trigger_number",tts]
_tlu = _tlu[maskt]

print(_kpix.columns)
maskk = ["Significance","trigN","runtime"]
_kpix = _kpix.drop(maskk, axis=1)

ts_names=[]
for i in np.unique(diffs):
    name="ts+"+str(i)
    ts_names.append(name)
    
    _tlu[name] = _tlu[tts].apply(lambda x: x+i)
#print (_tlu.head(3))

res_list=[]
for name in ts_names:
    res_i = pd.merge(_kpix, _tlu,
                     left_on=kts,
                     right_on=name)
    res_list.append(res_i)
# end of for loop 
res = pd.concat(res_list)
print(" How many matched triggers?",res['Event Number'].unique().size)



"""
 * Write into a PyGBL input.dat file: *

 Layer, x, y, z, Significance2, Size, Charge, runtime_ns
 ...
 Runnumber, TrigN, B-field
 Layer, x, y, z, Significance2, Size, Charge, runtime_ns
 ...

"""
# add x-pos, z-pos, drop un-necessary
list2drop = ts_names + ["ni_trigger_number", "Event Number", "timestamp_low", "event"]

res=res.drop(list2drop ,axis=1)
res.rename( columns = {'position': 'y-pos'}, inplace = True)
res.insert(1,'x-pos', 0.0)
res.insert(3,'z-pos', 0.0)

print(res.columns)
print(res.head(3))
f = open(f'res_{runnumber}.dat', 'w')

for i in (res['trigger'].unique()):
    if i<10:
        print (res[res.trigger==i].loc[:, res.columns != 'trigger'])
    #with open('res.dat', 'a') as f:
    f.write( res[res.trigger==i].loc[:, res.columns != 'trigger'].to_string( header = False, index=False) )
    f.write('\n%s %d %.1f\n'%(runnumber,i,args.bfield)) # add header line
