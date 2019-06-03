import numpy as np
from makeFigureS1 import makeFigureS1
from makeFigureS2 import makeFigureS2
import seaborn.apionly as sns
from netCDF4 import Dataset

class Formulation:
    def __init__(self):
        self.name = None
        self.resultfile = None
        self.bestHydro = None
        self.bestDeficit = None
        self.bestRecovery = None
        self.bestFlood = None
        self.bestStd = None
        
def getFormulations(name):
    formulation = Formulation()
    formulation.name = name
    formulation.resultfile = np.loadtxt('./../' + name + '/' + name + '_thinned.resultfile')
    formulation.bestHydro = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
        str(np.argmin(formulation.resultfile[:,176])+1) + '_re-eval_1x1000.nc')
    formulation.bestDeficit = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
        str(np.argmin(formulation.resultfile[:,177])+1) + '_re-eval_1x1000.nc')
    if name == 'WC':
        formulation.bestFlood = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(np.argmin(formulation.resultfile[:,178])+1) + '_re-eval_1x1000.nc')
    else:
        formulation.bestRecovery = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(np.argmin(formulation.resultfile[:,178])+1) + '_re-eval_1x1000.nc')
        formulation.bestFlood = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
            str(np.argmin(formulation.resultfile[:,179])+1) + '_re-eval_1x1000.nc')
        if name == 'EVSDH':
            formulation.bestStd = loadData('./../' + name + '/simulations/' + name + '_thinned_soln' + \
                str(np.argmin(formulation.resultfile[:,180])+1) + '_re-eval_1x1000.nc')
                
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
    
def plotSimulations():
    '''Makes Figure S1 and S2 from Quinn et al., 2016 - WRR \
    Figure S1 = Storage and Release Trajectories at Hoa Binh \
    Figure S2 = Storage Trajectories at all 4 Reservoirs'''
    
    sns.set_style("dark")
    
    WC = getFormulations('WC')
    WP1 = getFormulations('WP1')
    EV = getFormulations('EV')
    EVSDH = getFormulations('EVSDH')
    
    formulations = [WC, WP1, EV, EVSDH]
    colors = ['#1b9e77','#d95f02','#7570b3','#e7298a','#e6ab02']
    ylabels = [r'$s_t^{HB} (km^3\!)$',r'$r_t^{HB} (m^3\!/s)$']
    titles = ['WC Formulation', 'WP1 Formulation', 'EV Formulation', 'EV&SD$\mathregular{_H}$ Formulation']
    makeFigureS1(formulations, colors, ylabels, titles, 'FigureS1.pdf')
    
    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3']
    ylabels = [r'$s_t^{SL} (km^3\!)$',r'$s_t^{HB} (km^3\!)$',r'$s_t^{TQ} (km^3\!)$',r'$s_t^{TB} (km^3\!)$']
    makeFigureS2(formulations, colors, ylabels, 'FigureS2.pdf')
    
    return None

plotSimulations()
