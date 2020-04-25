# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:49:08 2020

@author: Nick Piacente

David --- use these two charts to paste to the screen
Import works!
"""

import getYahooData as yd

finalFrame, bestSelection = yd.getOptionsData(.9,7500)
#bidAskChart = yd.getDetailedQuote('DOW')

# make the stockPareto chart.  This should be done in the Tk program
stockParetoChart = stockPareto.plot(kind='scatter',x='POP',y='Potential Gain Multiple Contracts')