import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def makeFigure1():
    '''Makes Figure 1 from Quinn et al., 2017 - WRR (bar chart of time-varying \
    demand and pie chart of demand by sector)'''
    
    sns.set_style("dark")
    
    x = ['Cultivation','Livestock','Environment','Rural','Urban','Industry','Fishery']
    sizes = [58,1,7,2,2,1,29]
    labels = ['{0} - {1:1.0f} %'.format(i,j) for i,j in zip(x, sizes)]
    colors = ['#ff7f00','#fdbf6f','#33a02c','#b2df8a','#e31a1c','#fb9a99','#1f78b4']
    
    demand = np.loadtxt('RR_distributedIrrDemand.txt')
    demand = np.append(demand[121::],demand[0:121])
    
    width = 1.0
    bins = map(lambda x: x - width, range(1,366))
    
    fig = plt.figure()
    ax = plt.subplot2grid((1,3),(0,0),colspan=2)
    ax.bar(bins, demand, width=width, edgecolor='none',facecolor='k')
    ax.set_xticks([15,45,75,106,137,167,198,229,259,289,319,350])
    ax.set_xticklabels(['M','J','J','A','S','O','N','D','J','F','M','A'],fontsize=18)
    ax.set_xlabel('Month',fontsize=20)
    ax.tick_params(axis='both',labelsize=20)
    ax.set_ylabel('Demand (m$\mathregular{^3}\!$/s)',fontsize=20)
    ax.set_xlim([0,365])
    ax.set_title('Time-varying Demand',fontsize=24)
    
    ax = plt.subplot2grid((1,3),(0,2))
    patches, texts = ax.pie(sizes, colors=colors, shadow=False, startangle=90)
    ax.set_title('Demand by Sector',fontsize=24)
    ax.legend(patches, labels, loc='lower center',ncol=2,fontsize=14)
    plt.axis('equal')
    fig.set_size_inches([14.875,7.3375])
    fig.savefig('Figure1.pdf')
    fig.clf()

return None