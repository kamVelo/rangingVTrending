"""
functions to calculate ADX values from price data.
"""
import pandas as pd
import os

def getPriceData(symbol:str, historical=False):
    if not historical:
        df = pd.read_csv(os.path.join(symbol,"prices_1d.csv"))
        return df

def calcADX(symbol:str, period:int):
    prices = getPriceData(symbol).iloc[1:,:] # leave the dataset reversed because we need to go backwards anyway.


    #step 1: work out directional movement.
    for ind

if __name__ == '__main__':
    print(getPriceData("AAPL"))