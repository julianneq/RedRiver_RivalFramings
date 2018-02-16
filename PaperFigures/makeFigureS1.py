import math
import numpy as np
from matplotlib import pyplot as plt
 
def makeFigureS1(formulations, colors, ylabels, titles, filename):
    '''Makes Figure S1 from Quinn et al., 2017 - WRR (average storage and release\
    trajectories at Hoa Binh for best flood, hydro, deficit, and if applicable, \
    recovery and hydro std solutions from all formulations)'''
    
    ncols = len(formulations)
    nrows = 2 # first row = storage at HB (2nd element in list), 2nd row = release at HB (3rd element in list)
    time = range(0,365)
    ymaxs = [1E10,8000]
    ymins = [0.3E10,0]
    window = [7,30]
    
    fig = plt.figure()
    for i in range(nrows):
        for j in range(ncols):
            ax = fig.add_subplot(nrows, ncols, ncols*i+j+1)
            l1, = ax.plot(time, movingAvg(np.mean(formulations[j].bestHydro[2+i],axis=0),window[i]), linewidth=2, c=colors[0])
            l2, = ax.plot(time, movingAvg(np.mean(formulations[j].bestDeficit[2+i],axis=0),window[i]), linewidth=2, c=colors[1])
            l3, = ax.plot(time, movingAvg(np.mean(formulations[j].bestFlood[2+i],axis=0),window[i]), linewidth=2, c=colors[2])
            if j > 0: # not WC formulation
                l4, = ax.plot(time, movingAvg(np.mean(formulations[j].bestRecovery[2+i],axis=0),window[i]), linewidth=2, c=colors[3])
                if j == (ncols-1): # EVSDH formulation
                    l5, = ax.plot(time, movingAvg(np.mean(formulations[j].bestStd[2+i],axis=0),window[i]), linewidth=2, c=colors[4])
                    
            ax.set_xlim([time[0],time[-1]])
            ax.set_ylim([ymins[i],ymaxs[i]])
            ax.tick_params(axis='both',labelsize=14)
            ax.set_xticks([45,137,229,319])
            ax.set_yticks([ymins[i], ymins[i]+0.25*(ymaxs[i]-ymins[i]), ymins[i]+0.5*(ymaxs[i]-ymins[i]),\
                ymins[i]+0.75*(ymaxs[i]-ymins[i]), ymaxs[i]])
            if i == 0:
                ax.set_yticklabels([ymins[i]/(1E9), (ymins[i]+0.25*(ymaxs[i]-ymins[i]))/(1E9), (ymins[i]+0.5*(ymaxs[i]-ymins[i]))/(1E9),\
                    (ymins[i]+0.75*(ymaxs[i]-ymins[i]))/(1E9), ymaxs[i]/(1E9)])
                ax.tick_params(axis='x',which='both',labelbottom='off')
                ax.set_title(titles[j],fontsize=18)
            else:
                ax.set_xticklabels(['Jun','Sep','Dec','Mar'],fontsize=16)
                
            if j == 0:
                ax.set_ylabel(ylabels[i],fontsize=16)
            else:
                ax.tick_params(axis='y',which='both',labelleft='off')
                
    fig.subplots_adjust(bottom=0.2)
    fig.legend([l1, l2, l3, l4, l5],['Best Hydro','Best Deficit$\mathregular{^2}$', 'Best Flood', 'Best Recovery','Best Hydro Std'],\
        loc='lower center', ncol=3, fontsize=16, frameon=True)
    fig.set_size_inches([17.05,8.15])
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
