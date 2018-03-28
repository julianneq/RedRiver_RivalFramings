import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
 
def makeFigure8(WCcomp, WP1comp, xlabel, ylabel, titles, filename):
    '''Makes Figure 8 from Quinn et al., 2017 - WRR (probabilistic state space \
    diagram for compromise solutions from WC and WP1 formulations)'''
    
    ncols = 2 # 1st column = WC compromise, 2nd column = WP1 compromise
    nrows = 1
    ymax = 15
    ymin = 0
    xmin = 5
    xmax = 30
    
    # create matrix of probabilities
    # dimensions are 100 rows x 100 columns (rows span 0-15 m depth at Hanoi, columns span total storages)
    WCprob = getProbs(WCcomp[0],WCcomp[1], ymax, ymin)
    WP1prob = getProbs(WP1comp[0],WP1comp[1], ymax, ymin)
    
    # convert to log scale and find range for colorbar tick marks
    WCprob = np.log10(WCprob)
    WP1prob = np.log10(WP1prob)
    a = WCprob[WCprob > -np.inf]
    b = WP1prob[WP1prob > -np.inf]
    tickMin = min(np.min(a), np.min(b))
    tickMax = max(np.max(a), np.max(b))
    
    fig = plt.figure()
    for j in range(ncols):
        ax = fig.add_subplot(nrows,ncols,j+1)
        if j == 0:
            sm = ax.imshow(WCprob, cmap='RdYlBu_r',origin="upper", norm=mpl.colors.Normalize(vmin=tickMin, vmax=tickMax))
        else:
            sm = ax.imshow(WP1prob, cmap='RdYlBu_r',origin="upper", norm=mpl.colors.Normalize(vmin=tickMin, vmax=tickMax))
            
        ax.set_xticks(np.arange(0,100+100/5,100/5))
        ax.set_title(titles[j],fontsize=16)
        ax.set_xticklabels(np.arange(xmin, xmax+5, 5),fontsize=16)
        ax.set_yticks(np.arange(0,100+100/3,100/3))
            
        if j == 0:
            ax.set_yticklabels(np.arange(ymax,ymin-5,-5),fontsize=16)
            ax.set_ylabel(ylabel,fontsize=18)
        else:
            ax.tick_params(axis='y',which='both',labelleft='off')
            
        ax.set_ylim([100,0])
        alarm1, = ax.plot([0,100],[(1-6.0/15.0)*100.0,(1-6.0/15.0)*100.0],linestyle=':',c='k') # first alarm
        alarm2, = ax.plot([0,100],[(1-11.25/15.0)*100.0,(1-11.25/15.0)*100.0],linestyle='--',c='k') # second alarm
        dikeHeight, = ax.plot([0,100],[(1-13.4/15.0)*100.0,(1-13.4/15.0)*100.0],linewidth=2,c='k') # dike height
        
    fig.subplots_adjust(right=0.8, bottom=0.2)
    fig.legend([alarm1, alarm2, dikeHeight],['First Alarm', 'Second Alarm', 'Dike Height'], \
        loc='lower center', ncol=3, frameon=True)
    fig.text(0.5, 0.15, xlabel, va='center', ha='center', fontsize=16)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = fig.colorbar(sm, cax=cbar_ax, ticks=np.arange(-6,-1,1))
    cbar.ax.set_ylabel('Probability Density',fontsize=16)
    cbar.ax.set_yticklabels([r'$10^{-6}$',r'$10^{-5}$',r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$'],fontsize=16)
    fig.set_size_inches([10.0625, 5.2625])
    fig.savefig(filename)
    fig.clf()

    return None
    
def getProbs(s, h, ymax, ymin):
    probMatrix = np.zeros([100,100])
    xmax = 3E10
    xmin = 0.5E10
    yStep = (ymax-ymin)/np.shape(probMatrix)[0]
    xStep = (xmax-xmin)/np.shape(probMatrix)[1]
    for i in range(np.shape(s)[0]):
        for j in range(np.shape(s)[1]):
            # figure out which "box" the simulated s and h are in
            row = int(np.floor((ymax-h[i,j])/yStep))
            col = int(np.ceil((s[i,j]-xmin)/xStep))
            if row < np.shape(probMatrix)[0] and col < np.shape(probMatrix)[1]:
                probMatrix[row,col] = probMatrix[row,col] + 1
                
    # calculate probability of being in each box
    probMatrix = probMatrix/(np.shape(s)[0]*np.shape(s)[1])
    
    return probMatrix
