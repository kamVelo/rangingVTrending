import json
import pandas as pd
import requests as rq
import os
from string import ascii_letters
import io
import random
import numpy as np
import matplotlib.pyplot as plt
#TODO: setup historical data download.
def randomString(length = 6):
    alphas = list(ascii_letters) + list(range(0,10))
    word = ""
    for i in range(0,length):
        word += str(random.choice(alphas))
    return word


def downloadPriceData(symbol: str, interval:str, historical=False):
    """
    downloads price data for a given stock.
    :symbol: symbol of the stock.
    :period: the time period e.g 5min 15min 1h etc.
    :historical: data from 2 years or recent data
    :return: None, downloads price data into a csv.
    """

    if not historical:
        if interval !="daily":

            dset_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=%s&apikey=%s&datatype=csv&outputsize=full" % (symbol, interval,randomString())
        else:
            dset_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s&datatype=csv&outputsize=full" % (symbol, randomString(9))
            print("hello")
        content = rq.get(dset_url).content
        if not os.path.isdir(symbol):
            os.mkdir(symbol)
        with open(os.path.join(symbol, "prices_" + interval + ".csv"), "wb") as f:
            f.write(content)
    else:
        pass

def downloadData_DI(symbol:str, interval:str):
    period = 14
    if not os.path.isdir(symbol):
        os.mkdir(symbol)
    if interval == "1d":
        interval_formatted = "daily"
    else: interval_formatted = interval

    DIMinusUrl = "https://www.alphavantage.co/query?function=MINUS_DI&symbol=%s&interval=%s&time_period=%s&apikey=%s&outputsize=full&datatype=csv" % (symbol, interval_formatted,period,randomString(9))
    DIPlusUrl = "https://www.alphavantage.co/query?function=PLUS_DI&symbol=%s&interval=%s&time_period=%s&apikey=%s&outputsize=full&datatype=csv" % (symbol, interval_formatted, period, randomString(9))
    urls = [DIMinusUrl,DIPlusUrl]
    names = ["DIMinus", "DIPlus"]
    for i in range(0,len(urls)):
        content = rq.get(urls[i]).content
        with open(os.path.join(symbol, names[i] +"_" + interval + ".csv"), "wb") as f:
            f.write(content)
def createADX(symbol:str, interval:str):
    """
    creates the ADX file using DI data from alphavantage. Calculates for 14 days by default.
    :param symbol: symbol of stocks
    :param interval: i.e daily 15min 5min etc.
    :return: none - creates the file in the stock's folder.
    """
    period = 14
    df = pd.read_csv(os.path.join(symbol, "DIPlus_" + interval + ".csv")).iloc[::-1]
    df["MINUS_DI"] = pd.read_csv(os.path.join(symbol, "DIMinus_" + interval + ".csv")).iloc[::-1]["MINUS_DI"]
    df.index = range(0, len(df))
    DX_arr = []
    adx = []
    for index, row in df.iterrows():
        dx = calcDX(row["PLUS_DI"], row["MINUS_DI"])
        DX_arr.append(dx)
        if index < period:
            adx.append(np.NaN)
        else:
          adx.append(round(sum(DX_arr[index-period:index])/14,2))
    df["ADX"] = adx
    df.to_csv(os.path.join(symbol, "ADX_" + interval + ".csv"))

def calcDX(DIPlus:float, DIMinus:float):
    return ( abs(DIPlus - DIMinus) / abs(DIPlus + DIMinus) ) * 100



if __name__ == '__main__':
    symbol = input("stock name: ")
    interval = input("Interval: ")
    downloadPriceData(symbol, interval)
    downloadData_DI(symbol, interval)
    createADX(symbol, interval)


    """
    df = pd.read_csv(os.path.join(symbol, "ADX_1d.csv")).iloc[::-1].iloc[:, 1:]
    df.index = range(0,len(df))
    df["closes"] = pd.read_csv(os.path.join(symbol, "prices_1d.csv")).iloc[::-1]["close"]
    plt.plot(df.index, df["closes"], color="red", label="close price")
    plt.plot(df.index, df["ADX"], color="blue", label="ADX")
    plt.legend()
    plt.show()
    """