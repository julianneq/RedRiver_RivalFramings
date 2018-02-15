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
    formulation.bestHydro = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
        str(np.argmin(formulation.resultfile[:,176])+1) + '_re-eval_1x100000_new.txt')
    formulation.bestDeficit = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
        str(np.argmin(formulation.resultfile[:,177])+1) + '_re-eval_1x100000_new.txt')
    if name == 'ieee_synthetic':
        formulation.bestFlood = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
            str(np.argmin(formulation.resultfile[:,178])+1) + '_re-eval_1x100000_new.txt')
        compIndex = findCompromise(formulation.resultfile[:,-3:],1)
        formulation.compromise = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
            str(compIndex+1) + '_re-eval_1x100000_new.txt')
    else:
        formulation.bestFlood = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
            str(np.argmin(formulation.resultfile[:,179])+1) + '_re-eval_1x100000_new.txt')
        compIndex = findCompromise(formulation.resultfile[:,-4:],1)
        formulation.compromise = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
            str(compIndex+1) + '_re-eval_1x100000_new.txt')
        
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

def reshapeMatrices(textfile):
    values = np.loadtxt(textfile)
    values = np.transpose(np.reshape(values,[100000,2*365]))
    sTOT = np.zeros([100000,365])
    hLev = np.zeros([100000,365])
    for i in range(np.shape(hLev)[1]):
        sTOT[:,i] = values[2*i,:]
        hLev[:,i] = values[2*i+1,:]
        
    return [sTOT, hLev]

def plotShadedDensity():
    '''Makes Figures 9 and 10 from Quinn et al., 2017 - WRR \
    Figure 9: Time-varying PDFs of water level at Hanoi \
    Figure 10: Probabilistic state space diagrams of total storage and water level at Hanoi'''
    
    sns.set_style("dark")
    
    WC = getFormulations('ieee_synthetic')
    WP1 = getFormulations('first_pct_obj')
    
    WCformulations = [WC.bestFlood, WC.bestHydro, WC.compromise]
    WP1formulations = [WP1.bestFlood, WP1.bestHydro, WP1.compromise]
    
    ylabels = ['WC Formulation', 'WP1 Formulation']
    titles = ['Best Flood Solution','Best Hydro Solution', 'Compromise Solution']
    makeFigure9(WCformulations, WP1formulations, ylabels, titles, 'Figure9.pdf')
    
    titles = ['WC Compromise Solution', 'WP1 Compromise Solution']
    xlabel = r'$s^{TOT} (km^3\!)$'
    ylabel = r'$z^{HN} (m)$'
    makeFigure10(WC.compromise, WP1.compromise, xlabel, ylabel, titles, 'Figure10.pdf')

    return None
    
plotShadedDensity()