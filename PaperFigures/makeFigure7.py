import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
 
def makeFigure7(WCformulations, WP1formulations, ylabels, titles, filename):
    '''Makes Figure 7 from Quinn et al., 2017 - WRR (time-varying PDFs of water \
    level at Hanoi for best flood, hydro and compromise solutions from WC and \
    WP1 formulations)'''
    
    ncols = 3 # 1st column = best flood soln, 2nd column = best hydro soln, 3rd column = compromise
    nrows = 2 # 1st row = WC formulation, 2nd row = WP1 formulation
    ymax = 15
    ymin = 0
    
    # create matrix of probabilities
    # dimensions are 366 rows x 365 columns (rows span 0-15 m depth at Hanoi, columns span days of the year)
    WCprob = []
    WP1prob = []
    for j in range(len(WCformulations)):
        WCsoln_i = np.log10(getProbs(WCformulations[j][1]))
        WP1soln_i = np.log10(getProbs(WP1formulations[j][1]))
        a = WCsoln_i[WCsoln_i > -np.inf]
        b = WP1soln_i[WP1soln_i > -np.inf]
        if j == 0:
            tickMin = min(np.min(a), np.min(b))
            tickMax = min(np.max(a), np.max(b))
        else:
            tickMin = min(np.min(tickMin), min(np.min(a), np.min(b)))
            tickMax = max(np.max(tickMax), max(np.max(a), np.max(b)))
            
        WCprob.append(WCsoln_i)
        WP1prob.append(WP1soln_i)
    
    fig = plt.figure()
    for i in range(nrows):
        for j in range(ncols):
            ax = fig.add_subplot(nrows,ncols,ncols*i+j+1)
            if i == 0:
                sm = ax.imshow(WCprob[j], cmap='RdYlBu_r',origin="upper", norm=mpl.colors.Normalize(vmin=tickMin, vmax=tickMax))
            else:
                sm = ax.imshow(WP1prob[j], cmap='RdYlBu_r',origin="upper", norm=mpl.colors.Normalize(vmin=tickMin, vmax=tickMax))
                
            ax.set_xticks([45,137,229,319])
            if i == 0:
                ax.tick_params(axis='x',which='both',labelbottom='off')
                ax.set_title(titles[j],fontsize=16)
            else:
                ax.set_xticklabels(['Jun','Sep','Dec','Mar'],fontsize=16)
                
            if j == 0:
                ax.set_yticks(np.arange(0,366+366/3,366/3))
                ax.set_yticklabels(np.arange(ymax,ymin-5,-5),fontsize=16)
                ax.set_ylabel(ylabels[i],fontsize=16)
            else:
                ax.tick_params(axis='y',which='both',labelleft='off')
                
            ax.set_ylim([365,0])
            alarm1, = ax.plot([0,365],[(1-6.0/15.0)*365.0,(1-6.0/15.0)*365.0],linestyle=':',c='k') # first alarm
            alarm2, = ax.plot([0,365],[(1-11.25/15.0)*365.0,(1-11.25/15.0)*365.0],linestyle='--',c='k') # second alarm
            dikeHeight, = ax.plot([0,365],[(1-13.4/15.0)*365.0,(1-13.4/15.0)*365.0],linewidth=2,c='k') # dike height
        
    fig.subplots_adjust(right=0.8,bottom=0.2)
    fig.text(0.04, 0.5, r'$z_{HN} (m)$', va='center', rotation='vertical',fontsize=18)
    fig.legend([alarm1, alarm2, dikeHeight],['First Alarm', 'Second Alarm', 'Dike Height'], \
        loc='lower center', ncol=3, frameon=True)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = fig.colorbar(sm, cax=cbar_ax, ticks=np.arange(-4,0,1))
    cbar.ax.set_yticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$'],fontsize=16)
    cbar.ax.set_ylabel('Probability Density',fontsize=16)
    fig.set_size_inches([13.3875, 6.3625])
    fig.savefig(filename)
    fig.clf()

    return None
    
def getProbs(data):
    probMatrix = np.zeros([366,365])
    ymax = 15.0
    ymin = 0.0
    step = (ymax-ymin)/366.0
    for i in range(np.shape(probMatrix)[0]):
        for j in range(np.shape(probMatrix)[1]):
            count = ((data[:,j] < ymax-step*i) & (data[:,j] >= ymax-step*(i+1))).sum()
            probMatrix[i,j] = count/100000.0
            #if count >= 4: # only calculate probability if at least 4 points in a box, otherwise set to 0
            #    probMatrix[i,j] = count/100000.0
    
    return probMatrix
