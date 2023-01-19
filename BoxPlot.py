import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import os
import scikit_posthocs as sp
import statistics
from scipy.stats import shapiro, mannwhitneyu, kruskal, levene


### Box plots 

directory = '_qdMetrics'
metricFilename = 'qd_score'
gp = []
alps = []
meab = []
almeab = []
gpcd = []
alpscd = []
mecd = []
almecd = []
hyperab = []
hypercd = []
almeabcd = []
almecdab = []
almeabcdAB = []
almecdabCD = []

def readMeanData(filename, arr):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        file = open(f,'r')
        for line in file:
            score = float(line)
            arr.append(score)

def plot(data):
    fig = plt.figure(figsize =(5, 6))
    # Creating plot
    plt.boxplot(data, showmeans=True, meanline=True, showfliers=False)
    plt.xticks([x+1 for x in range(len(data))],labels,rotation=10)
    # plt.ylim(0,122)
    plt.title('QD Score CD')
    # show plot
    plt.show()

def shapiro_wilk(data):
    # normality test
    stat, p = shapiro(data)
    print('W-stat=%f, p=%f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
    else:
        print('Sample does not look Gaussian (reject H0)')

readMeanData(metricFilename + '_gp.stat', gp)
readMeanData(metricFilename + '_alps.stat', alps)
readMeanData(metricFilename + '_meab.stat', meab)
readMeanData(metricFilename + '_almeab.stat',almeab)
readMeanData(metricFilename + '_hyper.stat', hyperab)
readMeanData(metricFilename + '_almecdab-ab-top.stat', almecdab)
readMeanData(metricFilename + '_almeabcd-ab-pop.stat', almeabcdAB)

readMeanData(metricFilename + '_gpcd.stat', gpcd)
readMeanData(metricFilename + '_alpscd.stat', alpscd)
readMeanData(metricFilename + '_mecd.stat', mecd)
readMeanData(metricFilename + '_almecd.stat',almecd)
readMeanData(metricFilename + '_hypercd.stat', hypercd)
readMeanData(metricFilename + '_almeabcd.stat', almeabcd)

data = [mecd, almecd, almeabcd, hypercd]
labels = ['MAP-Elites','ALME-CD','ALME-ABCD', 'Hypercube']

# for d in data:
#     # print(shapiro(d)[1])
#     print(statistics.median(d))

print(levene(mecd, almecd))

# pval = sp.posthoc_dunn(data, p_adjust = 'holm')
# print(pval)
# print(pval < 0.05)

# plot(data)





