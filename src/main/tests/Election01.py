import sys
sys.path.insert(0,'..')
from template.correlation import Correlation

a = Correlation("./../../../data/Elections/LS-2014_ElectionResult-CandiateWise.xls")
a.plot()
