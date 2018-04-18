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

    def plot_corr(self, do_print = False):
        corr = self.data.corr()
        if do_print:
            print(corr)

        f, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
                    square=True, ax=ax)

        plt.show()

    # creates histogram for continuous X
    def plot_distribution(self, X, O=[], bin = 5, do_print = False):
        d = self.data.copy()
        for o in O:
            d = d[d[o[0]] == o[1]]

        x = d[X]

        if do_print:
            print(x)

        plt.hist(x, bin)
        plt.xlabel(x)
        plt.ylabel("Count")
        plt.title("Total = " + str(len(x)))
        plt.show()


    def plot_distribution_discrete(self, X, O=[], do_print = False, title = "Bar graph"):
        d = self.data.copy()
        for o in O:
            d = d[d[o[0]] == o[1]]

        x = d[X].value_counts()

        if do_print:
            print(x)

        #plt.hist(x, ["GEN","SC","ST"])

        a = []
        b = []
        c = []
        for x1, x2 in x.items():
            c.append(x1)
            b.append(x2)

        a = range(len(b))
        fig, ax = plt.subplots()
        plt.title(title)
        ax.bar(a, b, tick_label = c, align = "center")
        plt.show()
