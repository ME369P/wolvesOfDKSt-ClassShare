# getYahooData.py
# Date Created: 4/14/20
# Date Last Modified: 04/25/20
# By: Nick Piacente

# Functions for generating processed dataframes and plots
# For future plotting in a GUI environment
# important columns:
#
# 'Potential Gain' - this is the option contract price * 100
# 'POP' - this is the probability of profit. The
#
# Currently filtering options by budget = strike price * 100
# It takes a few seconds per stock to fetch data from the internet on my machine (NP)

from yahoo_fin import options
from yahoo_fin import stock_info
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime

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
    # hardcoded:
    #   options date - 5/1/2020
    #   stocks to pick from: All DOW stocks

    # date selection
    today = datetime.today()
    optionsDate = datetime(2020,5,7)
    t = ((optionsDate - today).days + ((optionsDate - today).seconds/86400))/365
    if printOutput:
        print('t = {}'.format(t))
    stockPareto = pd.DataFrame()

    if printOutput:
        print('Starting Data Capture')

    # initial data capture and processing
    for stock in stock_info.tickers_dow():

        # checks if there is an option during the particular week.
        try:
            individualOptionsData = options.get_puts(stock,date=optionsDate)
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
    stockPareto['POP'] = stats.norm.cdf((np.log(stockPareto['Current Price'] / stockPareto['Strike'] ) +
                                         ( (stockPareto['IV']**2) /2)*t) / (stockPareto['IV']*np.sqrt(t)))
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
    stockPareto = stockPareto.set_index('Contract Name')

    # this is the field which will show in the interactive plot
    stockPareto['printString'] = ('Stock: ' + stockPareto['Stock Name']+'\n'
                                  'Strike Price = $'+ round(stockPareto['Strike'],2).astype(str)+'\n'+
                                  'Current Price = $' + round(stockPareto['Current Price'],2).astype(str) + '\n' +
                                  'Potential Gain = $'+ round(stockPareto['Potential Gain Multiple Contracts'],2).astype(str)+'\n' + 
                                  'ROI = ' + round(((stockPareto['Potential Gain Multiple Contracts']/budget) * 100),2).astype(str) + '%\n' +
                                  'Probability of Profit = ' + round(stockPareto['POP'],2).astype(str))
    
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
        
    return stockPareto, bestPick



def getDetailedQuote(stock, ax1 = None):
    # get the detailded bid/ask quote data for charting
    # input : stock ticker of the option of interest
    # for use with bestPick frame:
    #   bestPick['Stock'] would be the input
    # output is a matplotlib AxesSubplot object

    #stockPutChain = options.get_puts(stock)
    currentPrice=stock_info.get_live_price(stock)
    #info = stock_info.get_quote_table(stock)

    stockOptions = options.get_puts(stock).plot(x='Strike',y=['Bid','Ask'],
                                                xlim=[.5*currentPrice,1.5*currentPrice],
                                                title='Bid/Ask Put Spread for {}'.format(stock), ax = ax1)
    stockOptions.axvline(currentPrice, color='green', ls='--')

    return stockOptions


if __name__ == '__main__':
    stockPareto, bestPick = getOptionsData(personalRiskTolerance, budget, printOutput = True)
    chart = getDetailedQuote('DOW')
