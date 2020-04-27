# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:49:08 2020

@author: Nick Piacente

David --- use these two charts to paste to the screen
Import works!
"""

import getYahooData as yd
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
plt.ion()

finalFrame, bestSelection = yd.getOptionsData(.9,7500)
#bidAskChart = yd.getDetailedQuote('DOW')

# make the stockPareto chart.  This should be done in the Tk program
# stockParetoChart = stockPareto.plot(kind='scatter',x='POP',y='Potential Gain Multiple Contracts')...stockPareto not defined....

# fig, ax = plt.subplots()
# ax.scatter(finalFrame['POP'], finalFrame['Potential Gain Multiple Contracts'])
# mplcursors.cursor(hover=True)
# plt.show()

# show contract name
ax = finalFrame.plot.scatter(x='POP',y='Potential Gain Multiple Contracts')
mplcursors.cursor(hover=True).connect(
    "add", lambda sel: sel.annotation.set_text(finalFrame.index[sel.target.index]))
plt.show()