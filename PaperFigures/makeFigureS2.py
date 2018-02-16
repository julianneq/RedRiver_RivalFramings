import math
import numpy as np
from matplotlib import pyplot as plt
 
def makeFigureS2(formulations, colors, ylabels, filename):
    '''Makes Figure S2 from Quinn et al., 2017 - WRR (average storage trajectories \
    at all 4 reservoirs for best flood and hydro solutions from each formulation)'''
    
    ncols = 2 # 1st column = best flood solution, 2nd column = best hydro solution
    nrows = 4 # 1st row = SL, 2nd = HB, 3rd = TQ, 4th = TB
    time = range(0,365)
    ymaxs = [1E10,1E10,2.4E9,3.4E9]
    ymins = [0.2E10,0.2E10,0.4E9,0.6E9]
    titles = ['Best Flood Solution','Best Hydro Solution']
    window = 7
    lines = []
    
    fig = plt.figure()
    for i in range(nrows):
        for j in range(ncols):
            ax = fig.add_subplot(nrows, ncols, ncols*i+j+1)
            for f in range(len(formulations)):
                if j == 0:
                    l1, = ax.plot(time, movingAvg(np.mean(formulations[f].bestFlood[i*2],axis=0),window), linewidth=2, c=colors[f])
                else:
                    l1, = ax.plot(time, movingAvg(np.mean(formulations[f].bestHydro[i*2],axis=0),window), linewidth=2, c=colors[f])
                    
                lines.append(l1)
                    
                ax.set_xlim([time[0],time[-1]])
                ax.set_ylim([ymins[i],ymaxs[i]])
                ax.tick_params(axis='both',labelsize=14)
                ax.set_xticks([45,137,229,319])
                ax.set_yticks([ymins[i], ymins[i]+0.25*(ymaxs[i]-ymins[i]), \
                    ymins[i]+0.5*(ymaxs[i]-ymins[i]),ymins[i]+0.75*(ymaxs[i]-ymins[i]), ymaxs[i]])
                if i != (nrows-1):
                    ax.tick_params(axis='x',which='both',labelbottom='off')
                else:
                    ax.set_xticklabels(['Jun','Sep','Dec','Mar'],fontsize=16)

                if j == 0:
                    ax.set_ylabel(ylabels[i],fontsize=16)
                    ax.set_yticklabels([ymins[i]/(1E9), (ymins[i]+0.25*(ymaxs[i]-ymins[i]))/(1E9), \
                        (ymins[i]+0.5*(ymaxs[i]-ymins[i]))/(1E9),(ymins[i]+0.75*(ymaxs[i]-ymins[i]))/(1E9), ymaxs[i]/(1E9)])
                else:
                    ax.tick_params(axis='y',which='both',labelleft='off')
                        
                if i == 0:
                    ax.set_title(titles[j])
                
    fig.subplots_adjust(bottom=0.2,wspace=0.4)
    fig.legend(lines[0:4],['WC Formulation','WP1 Formulation', 'EV Formulation', 'EV&SD$\mathregular{_H}\!$ Formulation'],\
        loc='lower center', ncol=2, fontsize=16, frameon=True)
    fig.set_size_inches([8.45, 10.825])
    fig.savefig(filename)
    fig.clf()
                
    return None
    
def movingAvg(series,window):
    movingAvg = np.zeros(len(series))
    
    # find number of days before current day to start averaging
    before = int(math.floor(window/2))

   # insert 'before' number of days before series (take from end of series)
    newSeries = np.insert(series,0,series[-before::])

    # append 'window-before-1' number of days after series (take from beginning of series)
    newSeries = np.append(newSeries,series[0:before])
    
    for i in range(len(series)):
        movingAvg[i] = np.sum(newSeries[i:(i+window)]/window)
    
    return movingAvg
