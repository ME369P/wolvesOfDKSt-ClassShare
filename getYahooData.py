# getYahooData.py
# Date Created: 4/14/20
# Date Last Modified: 04/21/20
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
personalRiskTolerance = .9
budget = 10000

def getOptionsData(personalRiskTolerance, budget, printOutput = 'True'):
    # get the up to date stock options pareto.
    # Currently hardcoded for the DOW stocks
    # inputs: personal risk tolerance, budget
    # outputs: 
    #   stockPareto DataFrame (all options within the budget)
    #   bestPick DataFrame (highest value return within risk tolerance)
    #   stockParetoChart (matplotlob AxesSubplot object of risk/reward tradeoff)
    
    
    
    
    # date selection
    # currently hardcoded, needs some updating
    # weeksOut = 5
    t = 11/365 #(weeksOut * 7)/365 # alternate date logic - needs work
    
    stockPareto = pd.DataFrame()
    
    if printOutput:
        print('Starting Data Capture')
    
    # initial data capture and processing
    for stock in stock_info.tickers_dow():
        
        # checks if there is an option during the particular week.
        try:
            # alternate week selection logic
            #optionsDate = options.get_expiration_dates(stock)[weeksOut-1]
            individualOptionsData = options.get_puts(stock,date='05/01/20')
            
            # capture stock, current price for each stock
            individualOptionsData['Stock Name'] = stock
            individualOptionsData['Current Price'] = stock_info.get_live_price(stock)
            # IV formatting to a number
            individualOptionsData['IV']= individualOptionsData['Implied Volatility'].str.slice_replace(-1,repl='').astype(float)/100
        
        # if not, skip the ticker
        except:
            if printOutput:
                print('No data from {}'.format(stock))
            continue
        
        # if successful at obtaining options data, fill DataFrame stockPareto with the values
        stockPareto = stockPareto.append(individualOptionsData)
        if printOutput:
            print('Data from {} collected'.format(stock))
    
    if printOutput:
        print('Data Capture Complete!')
    
    # bool logic to make sure options are worth investing in
    beingTraded = stockPareto['Volume'] != '-'
    asksExist = stockPareto['Ask'] != '-'
    bidsExist = stockPareto['Bid'] != '-'
    
    # filtering by bool logic
    stockPareto = stockPareto[beingTraded & asksExist & bidsExist]
    
    ####################################################
    ### formatting of key variables in the DataFrame ###
    ####################################################
    
    # POP derived from Black-Scholes model
    stockPareto['POP'] = stats.norm.cdf((np.log(stockPareto['Current Price'] / stockPareto['Strike'] ) + ( (stockPareto['IV']**2) /2)*t) / (stockPareto['IV']*np.sqrt(t)))
    stockPareto['Strike'] = stockPareto['Strike'].astype(float)
    stockPareto['Bid'] = stockPareto['Bid'].astype(float)
    stockPareto['Ask'] = stockPareto['Ask'].astype(float)
    
    # determine number of each contract that is in budget
    # potential gain is the average contract selling price ~ (bid / ask) * 100
    # potential gain multiple contracts - potential gain * number of contracts that can be sold within budget 
    stockPareto['contractsInBudget'] = np.floor(budget/(stockPareto['Strike']*100))
    stockPareto['Potential Gain'] = ((stockPareto['Ask'] + stockPareto['Bid'])/2) * 100
    stockPareto['Potential Gain Multiple Contracts'] = stockPareto['Potential Gain'] * stockPareto['contractsInBudget']
    
    ###########################
    ### plotting the pareto ###
    ###########################
    
    inBudget = stockPareto['contractsInBudget'] > 0
    isInteresting = stockPareto['Bid'] != 0
    #withinPersonalRiskTolerance = stockPareto['POP'] > personalRiskTolerance
    stockPareto = stockPareto[inBudget & isInteresting]
    stockPareto.set_index('Contract Name')
    
    stockParetoChart = stockPareto.plot(kind='scatter',x='POP',y='Potential Gain Multiple Contracts', legend = 'Stock Name')
    
    ####################
    ## Best Fit Logic ##
    ####################
    
    #notAboveRisk = stockPareto['POP'] < (personalRiskTolerance + .01)
    notBelowRisk = stockPareto['POP'] > (personalRiskTolerance)
    bestPick = stockPareto[notBelowRisk].sort_values(by='Potential Gain Multiple Contracts',ascending = False)
    bestPick = bestPick.loc[bestPick['Potential Gain Multiple Contracts'].idxmax()]
    
    if printOutput:
        print('The best OPTION is:')
        print(bestPick)
        
    return stockPareto, bestPick, stockParetoChart



def getDetailedQuote(stock):
    # get the detailded bid/ask quote data for charting
    # input : stock ticker of the option of interest
    # for use with bestPick frame:
    #   bestPick['Stock'] would be the input
    # output is a matplotlib AxesSubplot object
    
    #stockPutChain = options.get_puts(stock)
    currentPrice=stock_info.get_live_price(stock)
    #info = stock_info.get_quote_table(stock)
    
    stockOptions = options.get_puts(stock).plot(x='Strike',y=['Bid','Ask'], xlim=[.5*currentPrice,1.5*currentPrice],title='Bid/Ask Call Spread for {}'.format(stock))
    stockOptions.axvline(currentPrice, color='green', ls='--')

    return stockOptions


if __name__ == '__main__':
    #getOptionsData(personalRiskTolerance, budget, printOutput = False)
    charty = getDetailedQuote('DOW')