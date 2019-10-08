# lycorisSyncPy
Python based code to study lycoris syncing with mimosa via AIDA2020-TLU

## ChangeLog
2019-Oct-8

-- Refactorize the code + adding plots from mergerKpixTlu.py

2019-Jun-3

-- adding the new merger to print out a allhits.csv file according to Claus' GBL file reader.

## Manual

+ explorer.py

  * input: timestamp csv files input with arguments
  * output: produce a list of matched trigger ID in a csv file defined with "-v" option
  * Plot: time difference between TLU and KPiX triggers are shown.

+ mergerKpixTlu.py

  * input: csv files input with arguments - list of lycoris clusters, and a trigger ID mask from explorer.py output
  * output: produce a res_{runnumber}.dat file as input for Claus' PyGBL code, format see below:
  * Plots: on the side, simple plots based on the raw clusters are shown.
    Charge distribution of 3 layers
    Cluster y-pos distribution of 3 layers
    Cut applied is significance>7 && Charge<10[fC]


Format of OUTPUT.dat file:

```
#Layer, x-pos, y-pos, z-pos, Significance2, Size, Charge, runtime_ns
14  0.0  32100.0  0.0   4.41674  1   1.883720  1023528160
14  0.0 -36750.0  0.0   4.41039  1   0.651141  1023528160
14  0.0  39800.0  0.0   4.38755  1   5.375250  1023528160
14  0.0  39350.0  0.0   3.21886  1   3.440240  1023528160
14  0.0  30300.0  0.0   3.16870  1   1.134590  1023528160
......
# runnumber, trigN, 0.0
400 179 0.0 
```

Explanation for each variables:

| Var    | Comment  |
|-------:|:---------|
| Layer | 10-15 lycoris sensor layer (corresponding to kpix analysis sensor 0-5)   |
| x-pos | always 0.0  |
| y-pos | in [um], center of gravity of a cluster (charge weighted center)  |
| z-pos | always 0.0  |
| Significance2 | sum_of_signal/sum_of_noise  |
| Size | number of strips inside a cluster  |
| Charge | cluster charge  |
| runtime_ns | related exteran trigger timestamp using TLU common clk with a 64bit runtime counter.  |
| trigN | trigger ID as TLU trigger ID  |
| runnumber | eudaq2 runnumber  |
