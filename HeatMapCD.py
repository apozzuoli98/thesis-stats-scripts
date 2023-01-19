from cmath import isnan
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import os
import re


# Creates diversity heat maps 

directory = 'pred_prey_statsALMECDAB'
diversityFitnessMap = np.full((10,12),-1) # Highest fitness found per morphological niche
diversityNumberMap = np.zeros((10,12)) # Number of solutions found per morphological niche
diversityAvgMap = np.full((10,12),-1) # Avg fitness per morphological niche
coverageScorePerRun = []
qdScorePerRun = []

# Iterate only over the out.stat files
for i in range(1,31):
    coverageMap = np.full((10,12), -1)
    coverageScore = 0
    qdScore = 0
    for filename in os.listdir(directory):
        if 'job.0.alps.3.out2_'+str(i)+'.stat' in filename:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                file = open(f,"r")
                for line in file:
                    line = line.split()
                    # Stats about heatmap come at end of .stat file
                    if '.' in line[0]:
                        fitness = float(line[0])
                        fitness = 25-((1/fitness)-1)
                        if ('alps.0.' in filename or 'alps.2.' in filename):
                            bh = re.findall('(\d+)', line[1])
                            # Convert raw behaviour metric into cell coordinates
                            centralDist = int(bh[0])
                            if (len(bh) > 2):
                                preyDist = int(bh[2])
                            elif 'CD' in line[1]:
                                centralDist = 120
                                preyDist = int(bh[0])
                            else:
                                preyDist = 180
                        elif ('alps.1.' in filename or 'alps.3.' in filename):
                            # For comparing different maps
                            centralDist = float(line[5])
                            preyDist = float(line[6])
                            if isnan(preyDist):
                                preyDist = 0
                        else:
                            bh = re.findall('(\d+)', line[1])
                            centralDist = int(bh[4])
                            if (len(bh) > 6):
                                preyDist = int(bh[6])
                            elif 'CD' in line[1]:
                                centralDist = 120
                                preyDist = int(bh[4])
                            else:
                                preyDist = 180

                        # if fitness > 15 and centralDist > 90 and centralDist < 100 and preyDist > 110 and preyDist < 120:
                        #     print(str(i) + ' ' + line[1])

                        # Convert raw behaviour metric into cell coordinates
                        centralDist = int(centralDist/10)-3 if int(centralDist/10)-3 <= 9 else 9
                        preyDist = int(preyDist/10)-6 if int(preyDist/10)-6 <= 11 else 11

                        # clip for small values
                        if centralDist < 0:
                            centralDist = 0
                        if preyDist < 0:
                            preyDist = 0

                        if fitness > diversityFitnessMap[centralDist][preyDist]:
                            diversityFitnessMap[centralDist][preyDist] = fitness
                        # diversityAvgMap[centralDist][preyDist] = diversityAvgMap[centralDist][preyDist] + fitness
                        # diversityNumberMap[centralDist][preyDist] = diversityNumberMap[centralDist][preyDist]+1

                        if fitness > coverageMap[centralDist][preyDist]:
                            coverageMap[centralDist][preyDist] = fitness
       
    # For comparing map elites from different behaviour maps
    diversityAvgMap = diversityAvgMap + coverageMap
    for i in range(len(coverageMap)):
            for j in range(len(coverageMap[i])):
                if coverageMap[i][j] >= 0:
                    diversityNumberMap[i][j] += 1

    for row in coverageMap:
        for elite in row:
            if elite >= 0:
                coverageScore += 1
                qdScore += elite
    coverageScorePerRun.append(coverageScore)
    qdScorePerRun.append(qdScore)

# avg fitness per number of solutions found in morphological niche
diversityAvgMap = diversityAvgMap / diversityNumberMap
removeNoSolution = diversityNumberMap / diversityNumberMap
diversityFitnessMap = diversityFitnessMap / removeNoSolution
diversityNumberMap = diversityNumberMap / removeNoSolution
diversityAvgMap = diversityAvgMap / removeNoSolution




ylabels = ['<30', '40', '50', '60', '70', '80', '90', '100', '110', '120']
xlabels = ['<60', '70', '80', '90', '100', '110', '120', '130', '140', '150', '160','170','180']

# Highest fitness
heatmap = sb.heatmap(data=diversityFitnessMap, xticklabels=xlabels, 
            yticklabels=ylabels, 
            vmax=25, vmin=0, cmap='viridis', cbar_kws={'label': 'Fitness'})
plt.ylabel('Avg dist. from centroid')
plt.yticks(rotation=0) 
plt.xlabel('Avg dist. from prey')
plt.title('Highest Fitness ALME CDAB')
plt.ylim(0,10)
plt.show()

# number of solutions
heatmap = sb.heatmap(data=diversityNumberMap, xticklabels=xlabels, 
            yticklabels=ylabels, 
            vmax=30, vmin=0, cmap='viridis', cbar_kws={'label': '# Solutions'})
plt.ylabel('Avg dist. from centroid')
plt.yticks(rotation=0) 
plt.xlabel('Avg dist. from prey')
plt.title('Number of Solutions ALME CDAB')
plt.ylim(0,10)
plt.show()

# average fitness
heatmap = sb.heatmap(data=diversityAvgMap, xticklabels=xlabels, 
            yticklabels=ylabels, 
            vmax=15, vmin=0, cmap='viridis', cbar_kws={'label': 'Fitness'})
plt.ylabel('Avg dist. from centroid')
plt.yticks(rotation=0) 
plt.xlabel('Avg dist. from prey')
plt.title('Average Fitness ALME CDAB')
plt.ylim(0,10)
plt.show()

# f = open('coverage_score_almeabcd_ww.stat', 'x')
# for score in coverageScorePerRun:
#     f.write(str(score))
#     f.write('\n')
# f.close

# f = open('qd_score_almeabcd_ww.stat', 'x')
# for score in qdScorePerRun:
#     f.write(str(score))
#     f.write('\n')
# f.close