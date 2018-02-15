import numpy as np
from makeFigure6 import makeFigure6
from makeFigure7 import makeFigure7
import seaborn.apionly as sns

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
    formulation.bestHydro = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
        str(np.argmin(formulation.resultfile[:,176])+1) + '_re-eval_1x1000.txt')
    formulation.bestDeficit = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
        str(np.argmin(formulation.resultfile[:,177])+1) + '_re-eval_1x1000.txt')
    if name == 'ieee_synthetic':
        formulation.bestFlood = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
            str(np.argmin(formulation.resultfile[:,178])+1) + '_re-eval_1x1000.txt')
    else:
        formulation.bestRecovery = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
            str(np.argmin(formulation.resultfile[:,178])+1) + '_re-eval_1x1000.txt')
        formulation.bestFlood = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
            str(np.argmin(formulation.resultfile[:,179])+1) + '_re-eval_1x1000.txt')
        if name == 'exp+hydro_std_obj':
            formulation.bestStd = reshapeMatrices('./../' + name + '/simulations/' + name + '_thinned_proc' + \
                str(np.argmin(formulation.resultfile[:,180])+1) + '_re-eval_1x1000.txt')
                
    return formulation

def reshapeMatrices(textfile):
    values = np.loadtxt(textfile)
    values = np.transpose(np.reshape(values,[1000,8*365]))
    sSL = np.zeros([1000,365])
    rSL = np.zeros([1000,365])
    sHB = np.zeros([1000,365])
    rHB = np.zeros([1000,365])
    sTQ = np.zeros([1000,365])
    rTQ = np.zeros([1000,365])
    sTB = np.zeros([1000,365])
    rTB = np.zeros([1000,365])
    for i in range(np.shape(sSL)[1]):
        sSL[:,i] = values[8*i,:]
        rSL[:,i] = values[8*i+1,:]
        sHB[:,i] = values[8*i+2,:]
        rHB[:,i] = values[8*i+3,:]
        sTQ[:,i] = values[8*i+4,:]
        rTQ[:,i] = values[8*i+5,:]
        sTB[:,i] = values[8*i+6,:]
        rTB[:,i] = values[8*i+7,:]
        
    return [sSL, rSL, sHB, rHB, sTQ, rTQ, sTB, rTB]
    
def plotSimulations():
    '''Makes Figure 6 and 7 from Quinn et al., 2016 - WRR \
    Figure 6 = Storage and Release Trajectories at Hoa Binh \
    Figure 7 = Storage Trajectories at all 4 Reservoirs'''
    
    sns.set_style("dark")
    
    WC = getFormulations('ieee_synthetic')
    WP1 = getFormulations('first_pct_obj')
    EV = getFormulations('exp_obj')
    EVSDH = getFormulations('exp+hydro_std_obj')
    
    formulations = [WC, WP1, EV, EVSDH]
    colors = ['#1b9e77','#d95f02','#7570b3','#e7298a','#e6ab02']
    ylabels = [r'$s_t^{HB} (km^3\!)$',r'$r_t^{HB} (m^3\!/s)$']
    titles = ['WC Formulation', 'WP1 Formulation', 'EV Formulation', 'EV&SD$\mathregular{_H}$ Formulation']
    makeFigure6(formulations, colors, ylabels, titles, 'Figure6.pdf')
    
    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3']
    ylabels = [r'$s_t^{SL} (km^3\!)$',r'$s_t^{HB} (km^3\!)$',r'$s_t^{TQ} (km^3\!)$',r'$s_t^{TB} (km^3\!)$']
    makeFigure7(formulations, colors, ylabels, 'Figure7.pdf')
    
    return None