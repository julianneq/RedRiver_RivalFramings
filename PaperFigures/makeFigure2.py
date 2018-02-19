from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

def makeFigure2():
    '''Makes Figure 2a of Quinn et al., 2017 - WRR (Red River basin map);
    Red River model schematic in 2b drawn manually'''
    
    # set-up Vietnam basemap
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # plot basemap, rivers and countries
    m = Basemap(llcrnrlat=19.5,urcrnrlat=26.0,llcrnrlon=99.6,urcrnrlon=107.5,resolution='h')
    m.arcgisimage(service='World_Shaded_Relief')
    m.drawrivers(color='dodgerblue',linewidth=1.0,zorder=1)
    m.drawcountries(color='k',linewidth=1.25)
    
    # plot Red River basin
    m.readshapefile('./../GISdata/RedRiverBasin_WGS1984','Basin',drawbounds=False)
    patches = []
    for info, shape in zip(m.Basin_info, m.Basin):
        if info['OBJECTID'] == 1:
            patches.append(Polygon(np.array(shape), True))
            
    ax.add_collection(PatchCollection(patches, facecolor='0.33',edgecolor='0.5',alpha=0.5))
    
    # plot dams
    damsLatLong = np.loadtxt('DamLocations.csv',delimiter=',',skiprows=1,usecols=[1,2])
    x, y = m(damsLatLong[:,1], damsLatLong[:,0])
    m.scatter(x, y, c='k', s=150, marker='^')
    
    # plot Hanoi
    x, y = m(105.8342, 21.0278)
    m.scatter(x, y, facecolor='darkred', edgecolor='darkred', s=150)
    
    # label reservoirs and Hanoi
    plt.text(104.8, 21.0, 'Hoa Binh', fontsize=18, ha='center',va='center',color='k')
    plt.text(104.0, 21.7, 'Son La', fontsize=18, ha='center', va='center', color='k')
    plt.text(105.0, 21.95, 'Thac Ba', fontsize=18, ha='center', va='center', color='k')
    plt.text(105.4, 22.55, 'Tuyen Quang', fontsize=18, ha='center', va='center', color='k')
    plt.text(105.8, 21.2, 'Hanoi', fontsize=18, ha='center', va='center', color='k')
    
    # plot inset of greater geographic area
    axins = zoomed_inset_axes(ax, 0.1, loc=1)
    axins.set_xlim(90, 115)
    axins.set_ylim(8,28)
    
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    
    m2 = Basemap(llcrnrlat=8.0,urcrnrlat=28.0,llcrnrlon=90.0,urcrnrlon=115.0,resolution='l',ax=axins)
    m2.arcgisimage(service='World_Shaded_Relief')
    m2.drawcountries(color='k',linewidth=0.5)
    
    # plot Vietnam green in inset
    m2.readshapefile('./../GISdata/VN_borders_only_WGS1984','Vietnam',drawbounds=False)
    patches2 = []
    for info, shape in zip(m2.Vietnam_info, m2.Vietnam):
        if info['Joiner'] == 1:
            patches2.append(Polygon(np.array(shape), True))
            
    axins.add_collection(PatchCollection(patches2, facecolor='forestgreen',edgecolor='0.5',alpha=0.5))
    
    # shade Red River basin grey in inset       
    axins.add_collection(PatchCollection(patches, facecolor='0.33',edgecolor='0.5',alpha=0.5))
    
    # label countries
    plt.text(107.5, 25.5, 'China', fontsize=11, ha='center',va='center',color='k')
    plt.text(102.5, 20.2, 'Laos', fontsize=11, ha='center', va='center', color='k')
    plt.text(101.9, 15.5, 'Thailand', fontsize=11, ha='center', va='center', color='k')
    plt.text(96.5, 21.0, 'Myanmar', fontsize=11, ha='center', va='center', color='k')
    
    plt.annotate('Vietnam', xy=(108.0,14.0), xycoords='data', xytext=(5.0,20.0), textcoords='offset points', \
        color='k',arrowprops=dict(arrowstyle='-'),fontsize=11)
    plt.annotate('Cambodia', xy=(104.5,12.0), xycoords='data', xytext=(-60.0,-25.0), textcoords='offset points', \
        color='k',arrowprops=dict(arrowstyle='-'),fontsize=11)
    
    fig.set_size_inches([17.05, 8.15])
    fig.savefig('Figure2.pdf')
    fig.clf()

    return None

makeFigure2()
