import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import os
from numpy import inf, nan


### Plot avg fitness ###
directory = 'convergence'
gp = []
alps = []
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

# gp = adj2hits(np.array(gp))
# alps = adj2hits(np.array(alps))
labels = ['gp', 'alps']


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
 
# plotting the points
plt.plot(x, gp, label="GP")
plt.plot(x, alps[193-151:], label="ALPS")
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
