import numpy as np
from makeFigure9 import makeFigure9
from makeFigure10 import makeFigure10
import seaborn.apionly as sns

class Formulation:
    def __init__(self):
        self.name = None
        self.resultfile = None
        self.bestFlood = None
        self.bestHydro = None
        self.bestDeficit = None
        self.compromise = None
        
def getFormulations(name):
    formulation = Formulation()
    formulation.name = name
    formulation.resultfile = np.loadtxt('./../' + name + '/' + name + '_thinned.resultfile')
    formulation.bestHydro = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
        str(np.argmin(formulation.resultfile[:,176])+1) + '_re-eval_1x100000.nc')
    formulation.bestDeficit = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
        str(np.argmin(formulation.resultfile[:,177])+1) + '_re-eval_1x100000.nc')
    if name == 'WC':
        formulation.bestFlood = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(np.argmin(formulation.resultfile[:,178])+1) + '_re-eval_1x100000.nc')
        compIndex = findCompromise(formulation.resultfile[:,-3:],1)
        formulation.compromise = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(compIndex+1) + '_re-eval_1x100000.nc')
    else:
        formulation.bestFlood = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(np.argmin(formulation.resultfile[:,179])+1) + '_re-eval_1x100000_new.txt')
        compIndex = findCompromise(formulation.resultfile[:,-4:],1)
        formulation.compromise = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(compIndex+1) + '_re-eval_1x100000.nc')
        
    return formulation
    
def findCompromise(refSet, deficitIndex):
    # normalize objectives for calculation of compromise solution
    nobjs = np.shape(refSet)[1]
    normObjs = np.zeros([np.shape(refSet)[0],nobjs])
    for i in range(np.shape(refSet)[0]):
        for j in range(nobjs):
            # take the square root of the deficit so it's less skewed
            if j == deficitIndex:
                normObjs[i,j] = (np.sqrt(refSet[i,j])-np.mean(np.sqrt(refSet[:,j])))/np.std(np.sqrt(refSet[:,j]))
            else:
                normObjs[i,j] = (refSet[i,j]-np.mean(refSet[:,j]))/np.std(refSet[:,j])
    
    # find compromise solution (solution closest to ideal point)
    dists = np.zeros(np.shape(refSet)[0])
    for i in range(len(dists)):
        for j in range(nobjs):
            dists[i] = dists[i] + (normObjs[i,j]-np.min(normObjs[:,j]))**2
            
    compromise = np.argmin(dists)
    
    return compromise

def loadData(textfile):
    dataset = Dataset(file)
    sTOT = dataset.variables['sTOT'][:]
    hLev = dataset.variables['hLev'][:]
        
    return [sTOT, hLev]

def plotShadedDensity():
    '''Makes Figures 7 and 8 from Quinn et al., 2017 - WRR \
    Figure 7: Time-varying PDFs of water level at Hanoi \
    Figure 8: Probabilistic state space diagrams of total storage and water level at Hanoi'''
    
    sns.set_style("dark")
    
    WC = getFormulations('WC')
    WP1 = getFormulations('WP1')
    
    WCformulations = [WC.bestFlood, WC.bestHydro, WC.compromise]
    WP1formulations = [WP1.bestFlood, WP1.bestHydro, WP1.compromise]
    
    ylabels = ['WC Formulation', 'WP1 Formulation']
    titles = ['Best Flood Solution','Best Hydro Solution', 'Compromise Solution']
    makeFigure9(WCformulations, WP1formulations, ylabels, titles, 'Figure7.pdf')
    
    titles = ['WC Compromise Solution', 'WP1 Compromise Solution']
    xlabel = r'$s^{TOT} (km^3\!)$'
    ylabel = r'$z^{HN} (m)$'
    makeFigure10(WC.compromise, WP1.compromise, xlabel, ylabel, titles, 'Figure8.pdf')

    return None
    
plotShadedDensity()
