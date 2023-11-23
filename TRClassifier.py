import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display
from math import trunc

class TRClassifier:
    def __init__(self, symbol:str, interval:str):
        self.symbol = symbol
        self.interval = interval
        self.df = pd.read_csv(os.path.join(symbol, "prices_" + interval + ".csv")).iloc[::-1].iloc[:,1:]
        #self.df["ADX"] = pd.read_csv(os.path.join(symbol, "ADX_" + interval + ".csv")).iloc[::-1]["ADX"]
        ADX = pd.read_csv(os.path.join(symbol, "ADX_"+interval + ".csv"))
        minLength = min([len(self.df), len(ADX)])
        self.df = self.df.iloc[:minLength, :]
        ADX = ADX.iloc[:minLength, :]
        self.df["ADX"] = ADX["ADX"].values
        self.df.index = range(0,len(self.df))
    def plotPeriod(self,start:int, length:int):
        """
        plots price and adx for the period
        :param start: start of period
        :param length: end of period
        :return: none
        """

        end = start + length
        print(f"start: {start}")
        print(f"end: {end}")
        if start < 0 or end > len(self.df):
            raise ValueError
        fig = make_subplots(cols=1, rows=2, row_heights=[0.7,0.3])
        fig.add_trace(go.Ohlc(x=list(range(start,end)), open=self.df["open"].loc[start:end].astype(int), high=self.df["high"].loc[start:end].astype(int), low=self.df["low"].loc[start:end].astype(int), close=self.df["close"].loc[start:end].astype(int)), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(range(start,end)), y=self.df["ADX"].loc[start:end]), row=2, col=1)
        fig.show()

    def calcDiffAsPercent(self, currHigh:float, prevHigh:float, absolute=False):
        """
        calculates the percentage difference between current and previous high
        :return: percentage diff
        """
        diff = abs(currHigh - prevHigh)
        perc = round(diff/prevHigh*100,2)
        return perc
    def rollingHighColumn(self, series, period=7)->list:
        """
        this function creates a series of rolling-high data
        :param series: the data used to create the rolling-highs
        :param period: over how long the rolling highs are measured
        :return: series containing the rolling highs
        """

        highs = []
        prevVals = [] # this is a list containing the last k-values in the column
        for i in range(0, len(series)):
            prevVals.append(series[i])
            if len(prevVals) > period: del prevVals[0]
            highs.append(max(prevVals))
        return highs

    def kDifferences(self, series, k=3, absolute=False):
        """
        produces k columns containing 1st through to the k-th % differences between the values of a series of data
        :param series: series used for calculations
        :param k: i
        :return: list of lists
        """
        cols = [[np.NaN]*len(series)]*k
        for i in range(0, len(series)):
            currVal = series[i]
            for j in range(1, k+1):
                prev_index = i-j
                if prev_index < 0: # at i = 0, no differences can be calculated
                    continue
                else:
                    prevVal = series[prev_index] # gets previous val
                    # cols[j-1] gets the column for the jth difference, i.e j-1 = 0 for j = 1 and j=1 represents first diff
                    # cols[j-1][i] gets the specific cell corresponding to the ith row.
                    cols[j-1][i] = self.calcDiffAsPercent(currVal, prevVal, absolute)
        return cols






if __name__ == '__main__':
    k = 5
    c = TRClassifier("MSFT", "daily")
    nPeriods = 7
    c.df[f"{nPeriods} period highs"] = c.rollingHighColumn(c.df["close"], nPeriods)
    differences = c.kDifferences(c.df[f"{nPeriods} period highs"], k=k, absolute=True)
    for i in range(0, len(differences)):
        c.df[f"{i+1}th % periodic high change"] = differences[i]
    data = c.df["1th % periodic high change"]
    data = [val for val in data if str(val) != 'nan']
    from discreteModel import discreteModel as DM
    model = DM(data=data,nClasses=200)

    print(f"original Mean: {model.mean}")
    print(f"original Median: {model.median}")
    print(f"original Skew: {model.skew}")
    retained = model.removeOutliers(threshold=6)

    print(f"new Mean: {model.mean}")
    print(f"new Median: {model.median}")
    print(f"new Skew: {model.skew}")

    #model.plotHist("binom", binomProb=0.1)
    print(model.discreteProb(2.1))


