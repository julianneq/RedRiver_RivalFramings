import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from netCDF4 import Dataset

class Formulation:
    def __init__(self):
        self.name = None
        self.resultfile = None
        self.refSet = None
        self.bestHydro = None
        self.bestDeficit = None
        self.bestRecovery = None
        self.bestFlood = None
        self.bestStd = None
        self.compIndex = None
        self.compromise = None
        
def makeFigure6():
    '''Makes Figure 6 from Quinn et al., 2017 - WRR (parallel axes plots and \
    average storage trajectories of best flood, hydro and compromise solutions \
    from WC and WP1 formulations)'''
    
    # Load Pareto sets
    WC = getFormulations('WC')
    WP1 = getFormulations('WP1')
    
    formulations = [WC, WP1]
    xlabels = [['Hydro','Deficit$\mathregular{^2}$','Flooding\nDamages'],['Hydro','Deficit$\mathregular{^2}$','Flood','Recovery']]
    titles = ['WC Formulation','WP1 Formulation']

    fig = plt.figure()
    # first plot parallel axes plots in first column
    with sns.axes_style("white"):
        for i in range(len(formulations)):
            ax = fig.add_subplot(2,2,i+1)
            table = formulations[i].refSet
            mins = np.min(formulations[i].refSet,0)
            argmins = np.argmin(formulations[i].refSet,0)            
            maxs = np.max(formulations[i].refSet,0)
            compIndex = formulations[i].compIndex
            ax = parallel_coordinate(ax, table, mins, maxs, argmins, compIndex, xlabels[i], titles[i])
    
    # next, plot the storage trajectories in the second column
    # and the release trajectories in the third
    ylabel = r'$s_t^{HB} (km^3\!)$'
    with sns.axes_style("dark"):
        for i in range(len(formulations)):
                fig, l1, l2, l3 = plotTrajectories(fig, formulations[i], i, ylabel)
                
    fig.subplots_adjust(bottom=0.2)
    fig.legend([l1,l2,l3],['Best Hydro','Best Flood','Compromise'],loc='lower center',ncol=3,\
        fontsize=16, frameon=True)
    fig.set_size_inches([10.125, 8.3625])
    fig.savefig('Figure6.pdf')
    fig.clf()
    
    return None
        
def getFormulations(name):
    formulation = Formulation()
    formulation.name = name
    formulation.resultfile = np.loadtxt('./../' + name + '/' + name + '_thinned.resultfile')
    formulation.refSet = np.loadtxt('./../' + name + '/' + name + '_thinned.csv',delimiter=',',skiprows=1)
    formulation.bestHydro = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
        str(np.argmin(formulation.resultfile[:,176])+1) + '_re-eval_1x1000.nc')
    formulation.bestDeficit = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
        str(np.argmin(formulation.resultfile[:,177])+1) + '_re-eval_1x1000.nc')
    if name == 'WC':
        formulation.bestFlood = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(np.argmin(formulation.resultfile[:,178])+1) + '_re-eval_1x1000.nc')
        formulation.compIndex = findCompromise(formulation.resultfile[:,-3:],1)
        formulation.compromise = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(formulation.compIndex+1) + '_re-eval_1x1000.nc')
    else:
        formulation.bestRecovery = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(np.argmin(formulation.resultfile[:,178])+1) + '_re-eval_1x1000.nc')
        formulation.bestFlood = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(np.argmin(formulation.resultfile[:,179])+1) + '_re-eval_1x1000.nc')
        if name != 'EVSDH':
            formulation.compIndex = findCompromise(formulation.resultfile[:,-4:],1)
            formulation.compromise = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
                str(formulation.compIndex+1) + '_re-eval_1x1000.nc')
        else:
            formulation.bestStd = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
                str(np.argmin(formulation.resultfile[:,180])+1) + '_re-eval_1x1000.nc')
            formulation.compIndex = findCompromise(formulation.resultfile[:,-5:],1)
            formulation.compromise = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
                str(formulation.compIndex+1) + '_re-eval_1x1000.nc')
        
    return formulation

def loadData(file):
    dataset = Dataset(file)
    sSL = dataset.variables['sSL'][:]
    rSL = dataset.variables['rSL'][:]
    sHB = dataset.variables['sHB'][:]
    rHB = dataset.variables['rHB'][:]
    sTQ = dataset.variables['sTQ'][:]
    rTQ = dataset.variables['rTQ'][:]
    sTB = dataset.variables['sTB'][:]
    rTB = dataset.variables['rTB'][:]
        
    return [sSL, rSL, sHB, rHB, sTQ, rTQ, sTB, rTB]
    
def findCompromise(refSet, deficitIndex):
    # normalize objectives for calculation of best compromise solution
    nobjs = np.shape(refSet)[1]
    normObjs = np.zeros([np.shape(refSet)[0],nobjs])
    for i in range(np.shape(refSet)[0]):
        for j in range(nobjs):
            # take the square root of the deficit so it's less skewed
            if j == deficitIndex:
                normObjs[i,j] = (np.sqrt(refSet[i,j])-np.mean(np.sqrt(refSet[:,j])))/np.std(np.sqrt(refSet[:,j]))
            else:
                normObjs[i,j] = (refSet[i,j]-np.mean(refSet[:,j]))/np.std(refSet[:,j])
    
    # find best comprommise solution (solution closest to ideal point)
    dists = np.zeros(np.shape(refSet)[0])
    for i in range(len(dists)):
        for j in range(nobjs):
            dists[i] = dists[i] + (normObjs[i,j]-np.min(normObjs[:,j]))**2
            
    compromise = np.argmin(dists)
    
    return compromise
    
def parallel_coordinate(ax, table, mins, maxs, argmins, compIndex, xlabels, title):
    scaled = table.copy()
    for j in range(np.shape(scaled)[1]):
        scaled[:,j] = (table[:,j] - mins[j]) / (maxs[j] - mins[j])
        
    for i in range(np.shape(scaled)[0]):
        ys = scaled[i,:]
        xs = range(len(ys))
        if i != argmins[0] and i != argmins[2] and i != compIndex:
            ax.plot(xs, ys, c=[0.85, 0.85, 0.85], linewidth=2, alpha=0.2)
            
    ax.plot(xs, scaled[argmins[0],:], c='#1b9e77', linewidth=2) # best hydro solution
    ax.plot(xs, scaled[argmins[2],:], c='#7570b3', linewidth=2) # best flood solution
    ax.plot(xs, scaled[compIndex,:], c='#e6ab02', linewidth=2) # compromise solution
        
    ax.set_title(title,fontsize=16)
    ax.set_xticks(np.arange(0,np.shape(table)[1],1))
    ax.set_xticklabels(xlabels,fontsize=14)
    ax.tick_params(axis='y',which='both',labelleft='off',left='off',right='off')
    ax.tick_params(axis='x',which='both',top='off',bottom='off')
    
    # draw in axes
    for i in np.arange(0,np.shape(table)[1],1):
        ax.plot([i,i],[0,1],c='k')
    
    return ax
    
def plotTrajectories(fig, formulation, col, ylabel):
    time = range(0,365)
    ymax = 1E10
    ymin = 0.3E10
    
    ax = fig.add_subplot(2,2,col+3)
    l1, = ax.plot(time,np.mean(formulation.bestHydro[2],axis=0), linewidth=2, c='#1b9e77')
    l2, = ax.plot(time,np.mean(formulation.bestFlood[2],axis=0), linewidth=2, c='#7570b3')
    l3, = ax.plot(time,np.mean(formulation.compromise[2],axis=0), linewidth=2, c='#e6ab02')
        
    ax.set_xlim([time[0],time[-1]])
    ax.set_ylim([ymin,ymax])
    ax.tick_params(axis='both',labelsize=14)
    ax.set_xticks([45,137,229,319])
    ax.set_yticks(np.arange(ymin, ymax + 0.25*(ymax-ymin), 0.25*(ymax-ymin)))
    ax.set_xticklabels(['Jun','Sep','Dec','Mar'],fontsize=16)
    if col == 1:
        ax.tick_params(axis='y',which='both',labelleft='off')
    else:
        ax.set_ylabel(ylabel,fontsize=16)
        ax.set_yticklabels(np.arange(int(ymin), int(ymax + 0.25*(ymax-ymin)), int(0.25*(ymax-ymin))))
            
    ax.set_yticklabels(np.arange(ymin/(1E9), (ymax + 0.25*(ymax-ymin))/(1E9), 0.25*(ymax-ymin)/(1E9)))  
        
    return fig, l1, l2, l3
    
makeFigure6()
