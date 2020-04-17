# hrhwPhase1.py
# Date Created: 4/14/20
# Date Last Modified: 04/16/20
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


def getOptionsData(personalRiskTolerance, budget, t):
    """
    
    Parameters
    ----------
    personalRiskTolerance : float
        decimal of the allowable risk for the user
    budget : int
        Max amount of collatoral available to trade with
    t : int
        time until expiration date of option

    Returns
    -------
    tuple of pandas DataFrames
    (stockPareto, bestPick) 
    i.e. (all the available options data, top most profitable picks)

    """
    # user inputs
    # personalRiskTolerance = .9
    # budget = 10000
    # #weeksOut = 5
    # t = 15/365 #(weeksOut * 7)/365
    
    stockPareto = pd.DataFrame()
    
    print('Starting Data Capture')
    
    # initial data capture and processing
    for stock in stock_info.tickers_dow():
        
        try:
            #optionsDate = options.get_expiration_dates(stock)[weeksOut-1]
            individualOptionsData = options.get_puts(stock,date='05/01/20')
            individualOptionsData['Stock Name'] = stock
            individualOptionsData['Current Price'] = stock_info.get_live_price(stock)
            individualOptionsData['IV']= individualOptionsData['Implied Volatility'].str.slice_replace(-1,repl='').astype(float)/100
        except:
            print('No data from {}'.format(stock))
            continue
        #individualOptionsData['Stock Name'] = stock
        #individualOptionsData['Current Price'] = stock_info.get_live_price(stock)
        #individualOptionsData['IV']= individualOptionsData['Implied Volatility'].str.slice_replace(-1,repl='').astype(float)/100
        stockPareto = stockPareto.append(individualOptionsData)
        print('Data from {} collected'.format(stock))
    
    print('Data Capture Complete!')
    
    #stockPareto['Potential Gain'] = stockPareto['Last Price'] * 100
    
    beingTraded = stockPareto['Volume'] != '-'
    asksExist = stockPareto['Ask'] != '-'
    bidsExist = stockPareto['Bid'] != '-'
    
    stockPareto = stockPareto[beingTraded & asksExist & bidsExist]
    
    stockPareto['POP'] = stats.norm.cdf((np.log(stockPareto['Current Price'] / stockPareto['Strike'] ) + ( (stockPareto['IV']**2) /2)*t) / (stockPareto['IV']*np.sqrt(t)))
    stockPareto['Strike'] = stockPareto['Strike'].astype(float)
    stockPareto['Bid'] = stockPareto['Bid'].astype(float)
    stockPareto['Ask'] = stockPareto['Ask'].astype(float)
    stockPareto['contractsInBudget'] = np.floor(budget/(stockPareto['Strike']*100))
    stockPareto['Potential Gain'] = ((stockPareto['Ask'] + stockPareto['Bid'])/2) * 100
    stockPareto['Potential Gain Multiple Contracts'] = stockPareto['Potential Gain'] * stockPareto['contractsInBudget']
    
    inBudget = stockPareto['contractsInBudget'] > 0
    isInteresting = stockPareto['Bid'] != 0
    withinPersonalRiskTolerance = stockPareto['POP'] > personalRiskTolerance
    stockPareto = stockPareto[inBudget & isInteresting]
    stockPareto.set_index('Contract Name')
    
    stockPareto.plot(kind='scatter',x='POP',y='Potential Gain Multiple Contracts', legend = 'Stock Name')
    
    ####################
    ## Best Fit Logic ##
    ####################
    
    notAboveRisk = stockPareto['POP'] < (personalRiskTolerance + .01)
    notBelowRisk = stockPareto['POP'] > (personalRiskTolerance - .01)
    bestPick = stockPareto[notBelowRisk & notAboveRisk].sort_values(by='Potential Gain Multiple Contracts',ascending = False)
    bestPick = bestPick.loc[bestPick['Potential Gain Multiple Contracts'].idxmax()]
    
    print('The best OPTION is:')
    print(bestPick)
    return stockPareto, bestPick

def formatOptionsdataFrame(pareto_df):
    """
    

    Parameters
    ----------
    pareto_df : dataFrame
        All Options in selected stock index 

    Returns
    -------
    tickerGroup : list of dataFrames
        list of dataFrames from pareto_df grouped by ticker symbol

    """
    tickerGroup = []
    for ticker in pareto_df['Stock Name'].unique():
        tickerGroup.append(pareto_df[pareto_df['Stock Name'] == ticker])
        
    return tickerGroup







