from matplotlib import pyplot as plt
import numpy as np
import seaborn.apionly as sns

class Formulation:
    def __init__(self):
        self.name = None
        self.optim = None
        self.reeval_new_1000 = None
        self.reeval_old_50 = None
        self.reeval_new_100000 = None
        self.reeval_old_5000 = None

def makeFigure5():
    '''Makes Figure 5 from Quinn et al., 2017 - WRR (re-evaluation of solutions \
    from each formulation on the objectives of all other formulations over \
    streamflows from both optimization and out-of-sample validation)'''
    
    sns.set_style("dark")
    
    # load thinned reference sets from each problem formulation
    WC = getFormulations('WC')
    WP1 = getFormulations('WP1')
    EV = getFormulations('EV')
    EVSDH = getFormulations('EVSDH')
    
    # specify plotting parameters
    formulations = [EVSDH, EV, WP1, WC]
    colors = ['#984ea3','#4daf4a','#377eb8','#e41a1c']
    indices = [[0,1,2],[0,1,3,2],[4,5,7,6]]
    ylabels = ['WC Objectives','WP1 Objectives','EV&SD$\mathregular{_H}$ Objectives']
    precision = [[1,0,0],[1,0,2,1],[1,0,1,1]]
    names = ['WC Formulation', 'WP1 Formulation', 'EV Formulation', 'EV&SD$\mathregular{_H}$ Formulation']
    titles = [['WC Hydro (Gwh/day)', 'WC Deficit$\mathregular{^2}\!$ (m$\mathregular{^3}\!$/s)$\mathregular{^2}$', \
            'WC Flood (-)'],\
        ['WP1 Hydro (Gwh/day)', 'WP1 Deficit$\mathregular{^2}\!$ (m$\mathregular{^3}\!$/s)$\mathregular{^2}$', \
            'WP1 Flood\n(m above 11.25 m)', 'WP1 Recovery (days)'],\
        ['EV Hydro (Gwh/day)', 'EV Deficit$\mathregular{^2}\!$ (m$\mathregular{^3}\!$/s)$\mathregular{^2}$', \
            'EV&SD$\mathregular{_H}$\nHydro Std (Gwh/day)', 'EV Recovery (days)']]
    
    makePlots(formulations, colors, indices, ylabels, titles, precision, names, 'Figure5.pdf')
    
    return None
    
def getFormulations(name):
    formulation = Formulation()
    formulation.name = name
    formulation.optim = np.loadtxt('./../' + name + '/' + name + '_thinned.csv',delimiter=',',skiprows=1)
    formulation.reeval_new_1000 = np.loadtxt('./../' + name + '/' + name + '_thinned_re-eval_1000.obj')
    formulation.reeval_old_50 = np.loadtxt('./../' + name + '/' + name + '_thinned_re-eval_50x20.obj')
    formulation.reeval_new_100000 = np.loadtxt('./../' + name + '/' + name + '_thinned_re-eval_100000.obj')
    formulation.reeval_old_5000 = np.loadtxt('./../' + name + '/' + name + '_thinned_re-eval_5000x20.obj')
        
    # replace columns of optimized_new or optimized_old with actual values from optimization, not re-evaluation on same sample size
    if formulation.name != 'ieee_synthetic':    
        if formulation.name == 'first_pct_obj':
            indices = [0,1,3,2]
        elif formulation.name == 'exp_obj':
            indices = [4,5,3,6]
        elif formulation.name == 'exp+hydro_std_obj':
            indices = [4,5,3,6,7]
        
        formulation.reeval_new_1000[:,indices] = formulation.optim
        
    return formulation
    
def makePlots(formulations, colors, indices, ylabels, titles, precision, names, figName):
    
    fig = plt.figure()
    dots = []
    # loop through rows (WC, WP1, EV-SD_H)
    for j in range(3):
        # loop through columns representing each objective in formulation of row j
        for i in range(len(indices[j])):
            ax = fig.add_subplot(3,4,j*4+i+1)
            xmin = np.inf
            xmax = -np.inf
            ymin = np.inf
            ymax = -np.inf
            # plot each formulation
            for k in range(len(formulations)):
                if j == 0:
                    if formulations[k].name == 'ieee_synthetic':
                        x = formulations[k].optim[:,indices[j][i]]
                        y = formulations[k].reeval_old_5000[:,indices[j][i]]
                    else:
                        x = formulations[k].reeval_old_50[:,indices[j][i]]
                        y = formulations[k].reeval_old_5000[:,indices[j][i]]
                else:
                    x = formulations[k].reeval_new_1000[:,indices[j][i]]
                    y = formulations[k].reeval_new_100000[:,indices[j][i]]                    
                        
                dot = ax.scatter(x,y,color=colors[k])
                if i == 0 and j == 0:
                    dots.append(dot)
                    
                # find minimum and maximum x and y values
                if np.min(x) < xmin:
                    xmin = np.min(x)
                if np.max(x) > xmax:
                    xmax = np.max(x)
                if np.min(y) < ymin:
                    ymin = np.min(y)
                if np.max(y) > ymax:
                    ymax = np.max(y)
                    
            ax.plot([xmin,xmax],[xmin,xmax],c='k',linestyle='--')
            ax.set_xlim([xmin,xmax])
            ax.set_ylim([min(xmin,ymin),max(xmax,ymax)])
            ax.set_xticks([xmin,xmax])
            ax.set_yticks([min(xmin,ymin),max(xmax,ymax)])
            if i == 0:
                ax.set_ylabel(ylabels[j],fontsize=24)
                
            if precision[j][i] != 0:
                if i != 0:
                    ax.set_xticklabels([np.round(xmin,precision[j][i]),np.round(xmax,precision[j][i])],fontsize=18)
                    ax.set_yticklabels([np.round(min(xmin,ymin),precision[j][i]),np.round(max(xmax,ymax),precision[j][i])],fontsize=18)
                else:
                    ax.set_xticklabels([np.round(-xmin,precision[j][i]),np.round(-xmax,precision[j][i])],fontsize=18)
                    ax.set_yticklabels([np.round(-min(xmin,ymin),precision[j][i]),np.round(-max(xmax,ymax),precision[j][i])],fontsize=18)
            else:
                ax.set_xticklabels([int(xmin),int(xmax)],fontsize=18)
                ax.set_yticklabels([int(min(xmin,ymin)),int(max(xmax,ymax))],fontsize=18)
                
            ax.set_title(titles[j][i],fontsize=24)
            # add line for dike height on new flooding objective subplots
            if i == 2 and j>0:
                ax.plot([0,2.15],[2.15,2.15],'k')
                ax.plot([2.15,2.15],[0,2.15],'k')
                
    ax = fig.add_subplot(3,4,4)
    ax.legend(dots[::-1],names,loc='upper right',fontsize=24, frameon=True)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis='y',which='both',labelleft='off',left='off',right='off')
    ax.tick_params(axis='x',which='both',labelbottom='off',top='off',bottom='off')
    
    fig.text(0.5, 0.04, 'Objective Values in Optimization Set', ha='center',fontsize=24)
    fig.text(0.04, 0.5, 'Objective Values in Validation Set', va='center', rotation='vertical',fontsize=24)
    fig.subplots_adjust(wspace=0.3,hspace=0.3)
    fig.set_size_inches([24, 12.55])
    fig.savefig(figName)
    fig.clf()
    
    return None
