from matplotlib import pyplot as plt
import numpy as np
import seaborn.apionly as sns

def makeFigure3():
    '''Makes Figure 3 from Quinn et al., 2017 - WRR (flood damage function)'''
    
    sns.set_style("dark")
    h = np.arange(0,14.0,0.1)
    d = np.zeros(len(h))
    for i in range(len(h)):
        if h[i] <= 6:
            d[i] = 0
        elif h[i] > 6 and h[i] <= 11.25:
            d[i] = (h[i]-6)*750000/5.25
        else:
            d[i] = 1.50601636E6*h[i]**4 - 7.00078878E7*h[i]**3 + 1.21999573E9*h[i]**2 - 9.44555684E9*h[i] + 2.74132803E10
        
    fig = plt.figure()
    # plot damage function
    ax = fig.add_subplot(1,1,1)
    l1, = ax.plot([6,6],[0,1.50601636E6*13.9**4 - 7.00078878E7*13.9**3 + 1.21999573E9*13.9**2 - 9.44555684E9*13.9 + 2.74132803E10], \
        c='k', linestyle=':', linewidth=2) # first alarm line
    l2, = ax.plot([11.25,11.25],[0,1.50601636E6*13.9**4 - 7.00078878E7*13.9**3 + 1.21999573E9*13.9**2 - 9.44555684E9*13.9 + 2.74132803E10], \
        c='k', linestyle='--', linewidth=2) # second alarm line
    l3, = ax.plot([13.4,13.4],[0,1.50601636E6*13.9**4 - 7.00078878E7*13.9**3 + 1.21999573E9*13.9**2 - 9.44555684E9*13.9 + 2.74132803E10], \
        c='k', linewidth=2) # third alarm line
    ax.plot(h, d, c='#cb181d', linewidth=2) # damage function
    ax.set_ylim([0,1.50601636E6*13.9**4 - 7.00078878E7*13.9**3 + 1.21999573E9*13.9**2 - 9.44555684E9*13.9 + 2.74132803E10])
    ax.set_xlim([0,13.9])
    ax.set_xlabel(r'$z_{HN}$', fontsize=20)
    ax.set_ylabel('Damages (-)', fontsize=20)
    ax.set_title('Flooding Damages Function',fontsize=24)
    ax.tick_params(axis='both',labelsize=18)
    
    fig.subplots_adjust(bottom=0.2)
    fig.legend([l1, l2, l3],['First Alarm','Second Alarm','Dike Height'],loc='lower center',ncol=3,frameon=True,fontsize=20)
    fig.set_size_inches([9.1,7.4125])
    
    fig.savefig('Figure3.pdf')
    fig.clf()
    
    return None

makeFigure3()