import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import os
from numpy import inf, nan


### Plot avg fitness ###
directory = 'convergence'
gp = []
alps = []
meab = []
mecd = []
almeab = []
almecd = []
hyper = []
almeabcd = []
almecdab = []
lineNum = 0

def readMeanData(filename, arr, col):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        file = open(f,'r')
        for line in file:
            line = line.split()
            arr.append(float(line[col]))

# def adj2hits(data):
#     hits = 25-((1/data)-1)
#     hits[hits < 0] = 0
#     hits[hits == -inf] = 0
#     hits[np.isnan(hits)] = 0
#     return hits

readMeanData('out_full_gp.stat', gp, 1)
readMeanData('out_full_alps.stat', alps, 1)
readMeanData('out_full_meab.stat', meab, 1)
readMeanData('out_full_almeab.stat', almeab, 1)
readMeanData('out_full_mecd.stat', mecd, 1)
readMeanData('out_full_almecd.stat', almecd, 1)
readMeanData('out_full_hyper.stat', hyper, 1)
readMeanData('out_full_almeabcd.stat', almeabcd, 1)
readMeanData('out_full_almecdab.stat', almecdab, 1)

# gp = adj2hits(np.array(gp))
# alps = adj2hits(np.array(alps))
labels = ['ALME AB', 'ALME CD', 'Hypercube']


# x axis values
x_gp = list(range(0,151))
x_alps = list(range(0,151))
x_meab = list(range(0, 151))
x_almeab = list(range(0,151))
x_mecd = []
x_almecd = []
x_almeabcd = []
x_almecdab = []
x = list(range(0,151))
x = [i*1000 for i in x]
readMeanData('out_full_mecd.stat', x_mecd, 2)
readMeanData('out_full_almecd.stat', x_almecd, 3)
readMeanData('out_full_almeabcd.stat', x_almeabcd, 3)
readMeanData('out_full_almecdab.stat', x_almecdab, 3)
 
# plotting the points
# plt.plot(x, gp, label="GP")
# plt.plot(x, alps[193-151:], label="ALPS")
# plt.plot(x, meab, label="MAP-Elites AB")
plt.plot(x, almeab[415-302::2], label="ALME AB")
# plt.plot(x_mecd, mecd, label="MAP-Elites CD")
plt.plot(x_almecd[:351-40:2], almecd[351-311::2], label="ALME CD")
plt.plot(x_almeabcd[:351-40:2], almeabcd[351-311::2], label="ALME ABCD")
plt.plot(x_almecdab[:378-40:2], almecdab[378-338::2], label="ALME CDAB")
# plt.plot(x, hyper, label="Hypercube")
plt.legend()
 
# naming the x axis
plt.xlabel('Evaluations')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
# naming the y axis
plt.ylabel('Fitness')
 
# giving a title to my graph
plt.title('')
 
# function to show the plot
plt.show()