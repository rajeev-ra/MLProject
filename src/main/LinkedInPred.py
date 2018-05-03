import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression

data = pd.read_excel("./../../data/LinkedIn/FinalData.xlsx")

X = np.column_stack((data["DEGREE-OTHER"], data["DEGREE-BACH"], data["DEGREE-MAST"], data["DEGREE-MBA"],
                     data["COLLEGE"], data["TCS-START"], data["JOINING-EXP"], data['GENDER-MALE'],
                     data["LEADER"], data["MGR"], data["HR"], data["SE"]))

YT = list(data['DURATION'])

class LinkedIn:
    data = 0
    yh = ['1-2', '2-3', '3-5', '5-7', '7-10', '10-15', '15-20', '20-100']
    clf = [0,1,2,3,4,5,6,7]
    errStr = "Cannot predict"
    def __init__(self):
        self.data = pd.read_excel("./../../data/LinkedIn/FinalData.xlsx")
        d = self.data
        X = np.column_stack((d["DEGREE-OTHER"], d["DEGREE-BACH"], d["DEGREE-MAST"], d["DEGREE-MBA"],
                             d["COLLEGE"], d["TCS-START"], d["JOINING-EXP"], d['GENDER-MALE'],
                             d["LEADER"], d["MGR"], d["HR"], d["SE"]))
        for i in range(8):
            Y = list(d[self.yh[i]])
            self.clf[i] = RandomForestClassifier(n_estimators=2)
            self.clf[i].fit(X, Y)

    def Predict(self, x):
        Y = []
        y = [0,1,2,3,4,5,6,7]
        for i in range(8):
            y[i] = self.clf[i].predict(x)

        for j in range(len(x)):
            YT = self.errStr
            f = False
            for i in range(8):
                if 1 == y[i][j]:
                    if False == f:
                        f = 1
                        YT = self.yh[i]
                    else:
                        YT = YT + " or " + self.yh[i]
            Y.append(YT)

        return Y

    def IsCorrect(self, c, p):
        if p == self.errStr:
            return False
        else:
            S = p.split(' or ')
            for s in S:
                d = s.split('-')
                min = float(d[0])
                max = float(d[1])

                if c >= min and c <= max:
                    return True

        return False



l = LinkedIn()
Y = l.Predict(X)

r = 0
w = 0
n = 0

print("================")
print("Wrong predictions")
print("-----------------")
print("Correct\t  Predicted")
for y, t in zip(Y, YT):
    if l.errStr == y:
        n = n + 1
    elif l.IsCorrect(t, y):
        r = r + 1
    else:
        w = w + 1
        print("",t, "\t\t", y)

print("================")
print(r, "Correct  || ", w, "Wrong  || ", n, "Cannot predict")
