import sys
sys.path.insert(0,'..')
from template.correlation import Correlation

a = Correlation("./../../../data/cricket/raw/Player_Match.csv")
a.plot()
