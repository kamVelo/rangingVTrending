"""
This file contains the class for a discrete probability model
"""
from math import trunc

import matplotlib.pyplot as plt
from scipy.stats import skew, norm, chisquare, binom
import numpy as np
from math import sqrt, log

class discreteModel:
    def __init__(self,data:list,nClasses:int):
        self.data = [val for val in data if str(val) != "nan"]
        if self.data == []:
            raise Exception("No valid data has been provided")
        self.nClasses = nClasses

        self.calcStats()

    def calcStats(self):
        """
        this calculates all necessary figures initially
        :return:
        """
        # create histogram
        self.frequencies, self.bins = np.histogram(a=self.data, bins=self.nClasses)
        self.histogram = dict(zip(self.bins, self.frequencies))

        # create pdf
        self.pdf = {}
        self.genProbabilities()
        # measures of central tendency

        self.median  = np.median(self.data)
        self.mean = np.mean(self.data)
        self.variance = np.var(self.data)
        self.sd = sqrt(self.variance)

        # skew:
        self.skew = self.getSkew()
    def genIntHistogram(self):
        self.intData = [int(val) for val in self.data]
        bins = [i for i in range(1,max(self.intData)+1)]
        self.intFrequencies, self.intBins = np.histogram(a=self.intData, bins=bins)
        self.intHist = dict(zip(self.intBins, self.intFrequencies))
        self.intProbs = [val/sum(self.intFrequencies) for val in self.intFrequencies]

    def genProbabilities(self):
        """
        this function uses frequencies in histogram to generate a pdf:
        :return: none
        """
        for key in self.histogram:
            self.pdf[key] = self.histogram[key]/sum(self.frequencies)
    def plotHist(self,dist:str, binomProb=None):
        """
        plots the histogram
        :return:
        """
        plt.axvline(x=self.median, color="r")
        plt.axvline(x=self.mean, color="b")
        if dist=="norm":
            plt.stairs(self.pdf.values(), self.bins)
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, self.mean, self.sd)
            plt.plot(x, p)
        elif dist=="binom":
            self.genIntHistogram()
            plt.stairs(self.intProbs, self.intBins)
            x = self.intBins
            p = 1-binom.cdf(x,n=25, p=binomProb)
            plt.plot(x,p)
        else:
            plt.stairs(self.frequencies,self.bins)
        plt.show()
    def getSkew(self):
        return skew(self.data)

    def removeOutliers(self, threshold:float) -> float:
        """
        removes all the data greater in magnitude than a threshold
        :param threshold: see above
        :return: % of retained data
        """
        freq_0 = sum(self.frequencies)
        self.data = [val for val in self.data if abs(val) <= threshold and abs(val) > 0.1]

        self.calcStats()
        freq_1 = sum(self.frequencies)
        return round(freq_1/freq_0 * 100, 2) # return percentage of data retained
    def logTransform(self, base=2):
        self.data = [log(abs(val),base) for val in self.data]
        self.calcStats()
    def plotNormDist(self,lim=20):
        x = np.linspace(-lim,lim, 100)
        p = norm.pdf(x,self.mean, self.sd)
        plt.plot(x,p)
        plt.show()

    def goodnessOfFitNorm(self):
        exp = []
        keys = list(self.histogram.keys())
        for i in range(0,len(keys[:-1])):
            edge0 = keys[i]
            edge1 = keys[i+1]
            p = norm.cdf(edge1, self.mean, self.sd) - norm.cdf(edge0, self.mean, self.sd)
            freq = p * sum(self.frequencies)
            exp.append(freq)
        obs = list(self.frequencies.copy())
        exp += [0]
        print(sum(exp))
        print(sum(obs))
        print(obs)
        print(exp)
        assignIdx = -1
        for i in range(0, len(obs)):
            i = assignIdx + 1
            if i > len(obs)-1:
                continue
            totalObs = obs[i]
            totalExp = exp[i]
            combinedIdx = [i]
            j = i + 1
            while totalObs < 5 and j<len(obs):
                totalObs += obs[j]
                totalExp += exp[j]
                combinedIdx.append(j)
                j += 1
            assignIdx = combinedIdx.pop(-1)
            obs[assignIdx] = totalObs
            exp[assignIdx] = totalExp
            for idx in  combinedIdx:
                obs[idx] = "del"
                exp[idx] = "del"
        obs = [val for val in obs if val != "del"]
        exp = [val for val in exp if val != "del"]
        print(sum(exp))
        print(sum(obs))
        chi2, pVal = chisquare(obs,exp)
        print(chi2)
    def discreteProb(self, val:float):
        for i in range(0,len(self.pdf.keys())):
            currKey = self.pdf.keys()[i]
            nextKey = self.pdf.keys(i+1)
            if val>float(key):
                currKey = float(key)
                nextKey = float(self.)
                return self.pdf[key]




