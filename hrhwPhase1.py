# hrhwPhase1.py
# Date Created: 4/14/20
# Date Last Modified: XX
# By: Nick Piacente

# Get some kind of pareto from stocks to give to Ziam for Goal Programming
# stockPareto is a DataFrame with all of the options data from the DOW
# important columns:
#
# 'Potential Gain' - this is the option contract price * 100
# 'POP' - this is the probability of profit. The equation needs some work
#
# Currently filtering options by budget = strike price * 100
# It takes a few seconds per stock to fetch data from the internet on my machine (NP)

from yahoo_fin import options
from yahoo_fin import stock_info
import pandas as pd
import numpy as np
from scipy import stats

# user inputs
personalRiskTolerance = .5
budget = 20000

stockPareto = pd.DataFrame()

print('Starting Data Capture')

# initial data capture and processing
for stock in stock_info.tickers_dow():
    
    individualOptionsData = options.get_puts(stock)
    S = stock_info.get_live_price(stock)
    t = 3/365
    individualOptionsData['IV']= individualOptionsData['Implied Volatility'].str.slice_replace(-1,repl='').astype(float)/100
    stockPareto = stockPareto.append(individualOptionsData)
    print('Data from {} collected'.format(stock))

print('Data Capture Complete!')

stockPareto['Potential Gain'] = stockPareto['Last Price'] * 100
stockPareto['POP'] = stats.norm.cdf((np.log(S / stockPareto['Strike'] ) + ( (stockPareto['IV']**2) /2)*t) / (stockPareto['IV']*np.sqrt(t)))
stockPareto['Strike'] = stockPareto['Strike'].astype(float)

inBudget = stockPareto['Strike'] * 100 <= budget
stockPareto = stockPareto[inBudget]

stockPareto.plot(kind='scatter',x='POP',y='Potential Gain', xlim = [personalRiskTolerance-.3,personalRiskTolerance + .3])