import sys
sys.path.insert(0,'..')
from template.correlation import Correlation

a = Correlation("./../../../data/Elections/LS-2014_ElectionResult-CandiateWise.xls")
a.plot_corr(True)

a.plot_distribution("Candidate Age", [("Position", 1)],bin=10);

a.plot_distribution_discrete("Candidate Category", title = "Candidates filed nomination")

a.plot_distribution_discrete("Candidate Category", [("Position", 1)], title = "Winners")