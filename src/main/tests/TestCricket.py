import sys
sys.path.insert(0,'..')
from template.cricket import Cricket

a = Cricket()
b = a.PlayerData(15)
c = a.TeamName(1)
d = a.Captains()
print(d)

