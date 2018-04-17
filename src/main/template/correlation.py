import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os.path

class Correlation(object):
    file = ""
    X = []
    Y = ""
    data = None

    def __init__(self, file, X = None, Y = None):
        self.file = file
        if X:
            self.X = X
        if Y:
            self.Y = Y

        ext = os.path.splitext(file)[1].lower()

        if ext == ".csv":
            self.data = pd.read_csv(file)
        elif ext == ".xls" or ext == ".xlsx":
            self.data = pd.read_excel(file)

    def setX(self, X):
        self.X = X

    def setY(self, Y):
        self.Y = Y

    def plot(self, X = None, Y = None):
        corr = self.data.corr()
        print(corr)
        f, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
                    square=True, ax=ax)

        plt.show()

