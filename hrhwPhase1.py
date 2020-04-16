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
budget = 15000
weeksOut = 7
t = (weeksOut * 7)/365

stockPareto = pd.DataFrame()

print('Starting Data Capture')

# initial data capture and processing
for stock in stock_info.tickers_dow():
    
    try:
        optionsDate = options.get_expiration_dates(stock)[weeksOut+1]
        individualOptionsData = options.get_puts(stock,date=optionsDate)
    except:
        print('No data from {}'.format(stock))
        continue
    S = stock_info.get_live_price(stock)
    individualOptionsData['IV']= individualOptionsData['Implied Volatility'].str.slice_replace(-1,repl='').astype(float)/100
    stockPareto = stockPareto.append(individualOptionsData)
    print('Data from {} collected'.format(stock))

print('Data Capture Complete!')

#stockPareto['Potential Gain'] = stockPareto['Last Price'] * 100

beingTraded = stockPareto['Volume'] != '-'
asksExist = stockPareto['Ask'] != '-'
bidsExist = stockPareto['Bid'] != '-'

stockPareto = stockPareto[beingTraded & asksExist & bidsExist]

stockPareto['POP'] = 1-stats.norm.cdf((np.log(S / stockPareto['Strike'] ) + ( (stockPareto['IV']**2) /2)*t) / (stockPareto['IV']*np.sqrt(t)))
stockPareto['Strike'] = stockPareto['Strike'].astype(float)
stockPareto['Bid'] = stockPareto['Bid'].astype(float)
stockPareto['Ask'] = stockPareto['Ask'].astype(float)
stockPareto['contractsInBudget'] = np.floor(budget/(stockPareto['Strike']*100))
stockPareto['Potential Gain'] = ((stockPareto['Ask'] - stockPareto['Bid'])/2) * 100
stockPareto['Potential Gain Multiple Contracts'] = stockPareto['Potential Gain'] * stockPareto['contractsInBudget']

inBudget = stockPareto['contractsInBudget'] > 0
isInteresting = stockPareto['Bid'] != 0
withinPersonalRiskTolerance = stockPareto['POP'] > personalRiskTolerance
stockPareto = stockPareto[inBudget & isInteresting]

stockPareto.plot(kind='scatter',x='POP',y='Potential Gain Multiple Contracts')
