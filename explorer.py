import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tlu", default = "run000400_combined.csv",
                    help="tlu timestamps file .csv")
parser.add_argument("-k", "--kpix", default = "Run_20190721_234548.csv",
                    help="kpix timestamps file .csv")
parser.add_argument("-o", "--out", default = "matched_trigN_mask.csv",
                    help="outfile name")
args = parser.parse_args()
print(f" tlu file: {args.tlu}, kpix file: {args.kpix}")


kpix_name = "sampleRuntime_full_ns"
tlu_name = "timestamp_low"
mask_file = args.out

####
kpix = pd.read_csv(args.kpix)
tlu = pd.read_csv(args.tlu)

## TLU trigger ID starts from 1:
kpix.insert(loc=0, column='trigN', value=1+np.arange(len(kpix)))


##-- START align the start trigger: offline synced TLU+NI may start from TID!=0
#print(tlu.iloc[0,:])
tlu1sttrig= tlu.iloc[0,:]['trigger'] # select 'trigger' at row=0
print("TLU first trigger starts at TID = ", tlu1sttrig)
print("\tAny repeated TLU trigger?\n", res[res.duplicated(['trigger'])==True].sort_values('trigger'))

##-- END OF align the start trigger: kpix may starts later than TLU 
##-- Drop the no-synced triggers from kpix:
##!! needs to -1 because TID starts from 1, and index in kpix csv indicates trigger ID
kpix = kpix.drop(kpix.index[:(tlu1sttrig-1)])
kpix = kpix.drop(columns = ["diff_64_ns"])
#print(kpix[:2])

print ('Kpix recorded %i Triggers, while tlu recorded %i Triggers' % (len(kpix.index), len(tlu.index)))

kk = len(kpix.index)
tt = len(tlu.index)
trigs = kk if kk<tt else tt
#trigs = 150

kpix = kpix.iloc[ 0:trigs ] 
tskpix = np.array(kpix[kpix_name])
#print(tskpix)

tlu = tlu.iloc[0:trigs]
tstlu = np.array(tlu[tlu_name])
#print (tstlu)
#tlu['timestamp_low'].plot(kind='hist', bins=10)
#plt.xlabel('timestamp [ns]')
#plt.show()
#print (" Debug -- kpix has ", kpix.index, ",  tlu has ", tlu.index)

diffs = tskpix - tstlu

print( "time diff < 0: \n",np.where(diffs<0))  # get index

print( kpix.loc[kpix['trigN'].isin(range(25230, 25250)) ] )

#print (tstlu[2648:2655])
#print (diffs[8032:8033])

##-- TBD: the 'or' in where statement does not work like this:
#print("time diff !=135/110 \n", np.where((diffs!=135) | (diffs!=110)) ) 


# NEW! produce a trigN mask file by comparing KPiX to TLU timestamp:
trign = np.array(tlu.trigger)
trign = np.delete(trign, np.where(diffs<0))
print(' write to ', mask_file)
np.savetxt(mask_file, trign, delimiter='\n', fmt='%d')

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
