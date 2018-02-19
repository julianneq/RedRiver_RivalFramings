import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import pandas
import seaborn.apionly as sns

def makeFigure4():
    '''Makes Figure 4 from Quinn et al., 2017 - WRR (parallel axes of tradeoffs \
    for all four formulations)'''
    
    sns.set_style("dark")
    
    # load thinned reference sets from each problem formulation
    WC = np.loadtxt('./../WC/WC_thinned.csv',delimiter=',',skiprows=1)
    WP1 = np.loadtxt('./../WP1/WP1_thinned.csv',delimiter=',',skiprows=1)
    EV = np.loadtxt('./../EV/EV_thinned.csv',delimiter=',',skiprows=1)
    EVSDH = np.loadtxt('./../EVSDH/EVSDH_thinned.csv',delimiter=',',skiprows=1)
    
    # set plotting characteristics
    formulations = [WC, WP1, EV, EVSDH]
    labels = [['WC Hydro\n(Gwh/day)','WC Deficit$\mathregular{^2}$\n(m$\mathregular{^3}\!$/s)$\mathregular{^2}$','WC Flood\nDamages (-)'],\
        ['WP1 Hydro\n(Gwh/day)','WP1 Deficit$\mathregular{^2}$\n(m$\mathregular{^3}\!$/s)$\mathregular{^2}$','WP1 Flood\n(m above 11.25 m)','WP1 Recovery\n(days)'],\
        ['EV Hydro\n(Gwh/day)','EV Deficit$\mathregular{^2}$\n(m$\mathregular{^3}\!$/s)$\mathregular{^2}$','WP1 Flood\n(m above 11.25 m)','EV Recovery\n(days)'],\
        ['EV Hydro\n(Gwh/day)','EV Deficit$\mathregular{^2}$\n(m$\mathregular{^3}\!$/s)$\mathregular{^2}$','WP1 Flood\n(m above 11.25 m)','EV Recovery\n(days)','SD Hydro\n(Gwh/day)']]
    cmaps = ['Reds_r','Blues_r','Greens_r','Purples_r']
    titles = ['Worst Case (WC)', 'Worst 1st Percentile (WP1)','Expected Value (EV)',\
        'Expected Value & Hydro St Dev (EV&SD$\mathregular{_H}\!$)']
    precision = [[1,0,0],[1,0,2,1],[1,0,2,1],[1,0,2,1,1]]
    
    # make 2 x 2 subplot with parallel axes for each problem formulation
    plot(formulations, labels, precision, cmaps, titles, 'Figure4.pdf')
    
    return None
    
def plot(formulations, labels, precision, cmaps, titles, filename):
    fig = plt.figure()
    shadeIndex = [0,0,0,0]
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        table = pandas.DataFrame(formulations[i],columns=labels[i])
        mins = np.min(formulations[i],0)
        maxs = np.max(formulations[i],0)
        # round number of significant digits shown on objective labels
        for j in range(len(labels[i])):
            if precision[i][j] != 0:
                labels[i][j] = str(np.round(mins[j],precision[i][j])) + '\n' + labels[i][j]
            else:
                labels[i][j] = str(int(mins[j]))+ '\n' + labels[i][j]
            # don't show negative sign on maximization objectives
            if mins[j] < 0:
                labels[i][j] = labels[i][j][1:]
        parallel_coordinate(ax, table, mins, maxs, cmaps[i], shadeIndex[i], titles[i], labels[i], precision[i])
            
    fig.set_size_inches([15.7,11.4625])
    fig.tight_layout()
    fig.savefig(filename)
    
    return None
    
def parallel_coordinate(ax, table, mins, maxs, cmap, shadeIndex, \
    title, xlabels, precision):
        
    toplabels = []
    # round number of significant digits shown on objective labels
    for i in range(len(xlabels)):
        if precision[i] != 0:
            toplabels.append(str(np.round(maxs[i],precision[i])))
        else:
            toplabels.append(str(int(maxs[i])))
        if maxs[i] < 0:
            # don't show negative sign on maximization objectives
            toplabels[i] = toplabels[i][1:]
        
    cmap = matplotlib.cm.get_cmap(cmap)
    scaled = table.copy()
    index = 0
    for column in table.columns:
        scaled[column] = (table[column] - mins[index]) / (maxs[index] - mins[index])
        index = index + 1
    
    for solution in scaled.iterrows():
        ys = solution[1]
        xs = range(len(ys))
        ax.plot(xs, ys, c=cmap(ys[shadeIndex]), linewidth=2)
    
    ax.set_title(title,fontsize=16,y=1.1)
    ax.set_xticks(np.arange(0,np.shape(table)[1],1))
    ax.set_xticklabels(xlabels,fontsize=14)
    ax.tick_params(axis='y',which='both',labelleft='off',left='off',right='off')
    ax.tick_params(axis='x',which='both',top='off',bottom='off')
    
    # make subplot frames invisible
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    # draw in axes
    for i in np.arange(0,np.shape(table)[1],1):
        ax.plot([i,i],[0,1],c='k')
    
    # create twin y axis to put x tick labels on top
    ax2 = ax.twiny()
    ax2.set_xticks(np.arange(0,np.shape(table)[1],1))
    ax2.set_xticklabels(toplabels,fontsize=14)
    ax2.tick_params(axis='y',which='both',labelleft='off',left='off',right='off')
    ax2.tick_params(axis='x',which='both',top='off',bottom='off')
    
    # make subplot frames invisible
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    
    return ax

makeFigure4()
