import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

# Fixing random state for reproducibility
#np.random.seed(19680801)

#mu, sigma = 100, 15
#x = mu + sigma * np.random.randn(10000)
#print(type(x))
# # the histogram of the data
# n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)

####
tlu = pd.read_csv("run255_trigger.csv")
print(tlu.head())
tlu = tlu.iloc[0:100]
print(tlu['timestamp_low'])
tstlu = np.array(tlu['timestamp_low'])
print (tstlu)
#tlu['timestamp_low'].plot(kind='hist', bins=10)
#plt.xlabel('timestamp [ns]')
#plt.show()

#kpix = pd.read_csv("dumpkpix_trigger.csv")
kpix = pd.read_csv("Run_20190505_111442.csv")
kpix = kpix.iloc[0:100]
print(kpix.head())
print(kpix.info())
tskpix = np.array(kpix['TrigTimestamp_ns'])

diffs = tskpix - tstlu
print(diffs)
xmin = np.amin(diffs)-10
xmax = np.amax(diffs)+10
if (xmax-xmin)%5!=0:
    print("ERROR: check your data!")
    exit()
nbins = int((xmax-xmin)/5)
print("nbins = ", nbins, "; xmin, xmax = ", xmin, xmax)

n, bins, patches = plt.hist(diffs, nbins, range=(xmin,xmax), density=False, facecolor='g', alpha=0.75)

plt.xlabel('Timestamp [ns]')
plt.ylabel('Ab.')
plt.title('Histogram')
#plt.grid(True)
plt.show()
