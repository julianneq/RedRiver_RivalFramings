from makeFigure2 import makeFigure2
from makeFigure3 import makeFigure3
from makeFigure4 import makeFigure4
from makeFigure5 import makeFigure5
from makeFigure6 import makeFigure6
from plotShadedDensity import plotShadedDensity
from plotSimulations import plotSimulations

def makeAllFigures():
  
  makeFigure2()
  makeFigure3()
  makeFigure4()
  makeFigure5()
  makeFigure6()
  plotSimulations() # makes Figures 7 and 8
  plotShadedDensity() # makes Figures S1 and S2
  
  return None

makeAllFigures()
