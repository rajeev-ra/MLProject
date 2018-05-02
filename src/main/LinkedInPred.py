import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

data = pd.read_excel("./../../data/LinkedIn/FinalData.xlsx")

X = np.column_stack((data["DEGREE-OTHER"], data["DEGREE-BACH"], data["DEGREE-MAST"], data["DEGREE-MBA"],
                     data["COLLEGE"], data["TCS-START"], data["JOINING-EXP"], data['GENDER-MALE'],
                     data["LEADER"], data["MGR"], data["HR"], data["SE"]))

Y = list(data['1-2'])

clf = RandomForestClassifier(n_estimators=2)
clf.fit(X, Y)

y = clf.predict(X)

s = 0
d = 0
for a, b in zip(Y, y):
    if a == b:
        s = s+1
        #print("Same", a)
    else:
        d = d+1
        #print("Different", a, b)

print (s, " Same  ||  ", d, " Different")
print(clf.score(X, Y))
