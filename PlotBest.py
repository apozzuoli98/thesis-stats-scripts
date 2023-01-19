from traceback import format_exc
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import scikit_posthocs as sp
import os
import statistics
from scipy.stats import shapiro, mannwhitneyu, kruskal, levene

### Box plots 

directory = 'bestOfRun'
gp = []
alps = []
meab = []
mecd = []
almeab = []
almecd = []
hyper = []
almeabcd = []
almecdab = []
forMeab = []
forMecd = []
forHyper = []
forAlmeabcd = []
forAlmecdab = []
meabww = []
mecdww = []
almecdabww = []
almeabcdww =[]

def readMeanData(filename, arr):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        file = open(f,'r')
        for line in file:
            if '.' in line:
                arr.append(float(line))


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

def mann_whitney(x, y):
    stat, p_value = mannwhitneyu(x, y)
    print('Statistics=%f, p=%f' % (stat, p_value))
    # Level of significance
    alpha = 0.05
    # conclusion
    if p_value < alpha:
        print('Reject Null Hypothesis (Significant difference between two samples)')
    else:
        print('Do not Reject Null Hypothesis (No significant difference between two samples)')


def plot(data):
    fig = plt.figure(figsize =(5, 5))
    
    # Creating plot
    plt.boxplot(data, showmeans=True, meanline=True, showfliers=False)
    plt.xticks([x+1 for x in range(len(data))],labels, rotation=15)
    plt.ylim(10,26)
    plt.title('Global Performance')
    
    # show plot
    plt.show()

readMeanData('best_end_gp.stat', gp)
readMeanData('best_end_alps.stat', alps)
readMeanData('best_end_meab.stat', meab)
readMeanData('best_end_mecd2.stat', mecd)
readMeanData('best_end_almeab.stat',almeab)
readMeanData('best_end_almecd2.stat', almecd)
readMeanData('best_end_hyper.stat', hyper)
readMeanData('best_end_ALMEABCD.stat', almeabcd)
readMeanData('best_end_ALMECDAB.stat', almecdab)
readMeanData('best_end_foraging_meab.stat', forMeab)
readMeanData('best_end_foraging_mecd.stat', forMecd)
readMeanData('best_end_foraging_hyper.stat', forHyper)
readMeanData('best_end_foraging_almeabcd.stat', forAlmeabcd)
readMeanData('best_end_foraging_almecdab.stat', forAlmecdab)
readMeanData('best_end_meab_ww.stat', meabww)
readMeanData('best_end_mecd_ww.stat', mecdww)
readMeanData('best_end_almecdab_ww.stat', almecdabww)
readMeanData('best_end_almeabcd_ww.stat', almeabcdww)


data = [meab, mecd, hyper, almecdab, almeabcd]
labels = ['MAP-Elites AB', 'MAP-Elites CD', 'MAP-Elites 4D', 'ALME-CDAB', 'ALME-ABCD']
for i in range(len(data)):
    data[i] = np.array(data[i])
    data[i] = 25-((1/data[i])-1)


plot(data)
# for d in data:
#     print(statistics.kruskal(d))

# print(levene(meabww, mecdww, almeabcdww, almecdabww))
print(kruskal(meab, mecd, hyper, almecdab, almeabcd))
pval = sp.posthoc_dunn(data, p_adjust = 'holm')
print(pval)
print(pval < 0.05)