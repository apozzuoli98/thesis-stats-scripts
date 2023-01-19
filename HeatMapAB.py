import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import os
import re
from mpl_toolkits import mplot3d


# Creates diversity heat maps 

directory = 'pred_prey_statsAB'
diversityFitnessMap = np.full((10,10),-1) # Highest fitness found per morphological niche
diversityNumberMap = np.zeros((10,10)) # Number of solutions found per morphological niche
diversityAvgMap = np.full((10,10),-1) # Avg fitness per morphological niche
coverageScorePerRun = []
qdScorePerRun = []

for i in range(1,31):
    coverageMap = np.full((10,10), -1)
    coverageScore = 0
    qdScore = 0
    for filename in os.listdir(directory):
        if  'out2_'+str(i)+'.stat' in filename:#'job.0.alps.3.' in filename and
            f = os.path.join(directory, filename)
            
            if os.path.isfile(f):
                file = open(f,"r")
                for line in file:
                    line = line.split()
                    fitness = float(line[0])
                    fitness = 25-((1/fitness)-1)
                    if  ('alps.1' in filename or 'alps.3' in filename):
                        bh = re.findall('(\d+)', line[1])
                        turns = int(bh[0])
                        arenaCvg = int(bh[2]) ## everything after decimal is put into bh[1] (eg. T3500.0 -> bh['3500', '0'])
                        # Convert raw behaviour metric into cell coordinates
                        # 3500 is upper bound for tenth cell (index 9) and should be included in the tenth cell
                        turns = int(turns/350)-1 if int(turns/350) <= 9 else 9
                        arenaCvg = int(arenaCvg/350)-1 if int(arenaCvg/350) <= 9 else 9
                    elif ('alps.0' in filename or 'alps.2' in filename):
                        # For comparing different maps
                        turns = int(line[3])
                        arenaCvg = int(line[4])
                        # if (fitness > 18 and turns > 2800 and arenaCvg > 2100 and arenaCvg <= 3150): 
                        #     print(str(i) + " " + line[1])
                        turns = int(turns/350) if int(turns/350) <= 9 else 9
                        arenaCvg = int(arenaCvg/350) if int(arenaCvg/350) <= 9 else 9
                    else:
                        bh = re.findall('(\d+)', line[1])
                        turns = int(bh[0])
                        arenaCvg = int(bh[2]) ## everything after decimal is put into bh[1] (eg. T3500.0 -> bh['3500', '0'])
                        # Convert raw behaviour metric into cell coordinates
                        # 3500 is upper bound for tenth cell (index 9) and should be included in the tenth cell
                        turns = int(turns/350)-1 if int(turns/350) <= 9 else 9
                        arenaCvg = int(arenaCvg/350)-1 if int(arenaCvg/350) <= 9 else 9


                    if fitness > diversityFitnessMap[turns][arenaCvg]:
                        diversityFitnessMap[turns][arenaCvg] = fitness
                    # diversityAvgMap[turns][arenaCvg] = diversityAvgMap[turns][arenaCvg] + fitness
                    # diversityNumberMap[turns][arenaCvg] = diversityNumberMap[turns][arenaCvg]+1

                    if fitness > coverageMap[turns][arenaCvg]:
                        coverageMap[turns][arenaCvg] = fitness
        
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


xlabels = ['<350', '700', '1050', '1400', '1750', '2100', '2450', '2800', '3150', '3500']

ax = plt.axes(projection='3d')
_y = np.arange(len(diversityFitnessMap))
_x = np.arange(len(diversityFitnessMap[0]))
(x ,y) = np.meshgrid(_x,_y)
ax.plot_surface(x,y,diversityFitnessMap, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.set_ylabel('Behaviour 1')
ax.set_xlabel('Behaviour 2')
ax.set_zlabel('Fitness')
plt.show()

# Highest fitness
# heatmap = sb.heatmap(data=diversityFitnessMap, xticklabels=xlabels, 
#             yticklabels=xlabels, 
#             vmax=25, vmin=0, cmap='viridis', cbar_kws={'label': 'Fitness'})
# plt.ylabel('# Turns')
# plt.yticks(rotation=0) 
# plt.xlabel('Arena Coverage')
# plt.title('Highest Fitness Per Behavioural Niche ALME CDAB')
# plt.ylim(0,10)
# plt.show()

# Number of solutions
# heatmap = sb.heatmap(data=diversityNumberMap, xticklabels=xlabels, 
#             yticklabels=xlabels, 
#             vmax=30, vmin=0, cmap='viridis', cbar_kws={'label': '# Solutions'})
# plt.ylabel('# Turns')
# plt.yticks(rotation=0) 
# plt.xlabel('Arena Coverage')
# plt.title('Number of Solutions Per Behavioural Niche ALME CDAB')
# plt.ylim(0,10)
# plt.show()

# # Average Fitness
# heatmap = sb.heatmap(data=diversityAvgMap, xticklabels=xlabels, 
#             yticklabels=xlabels, 
#             vmax=15, vmin=0, cmap='viridis', cbar_kws={'label': 'Fitness'})
# plt.ylabel('# Turns')
# plt.yticks(rotation=0) 
# plt.xlabel('Arena Coverage')
# plt.title('Average Fitness Per Niche ALME CDAB')
# plt.ylim(0,10)
# plt.show()

# f = open('coverage_score_almeabcd_ab_ww.stat', 'x')
# for score in coverageScorePerRun:
#     f.write(str(score))
#     f.write('\n')
# f.close

# f = open('qd_score_almeabcd_ab_ww.stat', 'x')
# for score in qdScorePerRun:
#     f.write(str(score))
#     f.write('\n')
# f.close