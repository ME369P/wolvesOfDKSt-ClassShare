# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:49:08 2020

@author: Nick Piacente

David --- use these two charts to paste to the screen
Import works!
"""

import getYahooData as yd

finalFrame, bestSelection = yd.getOptionsData(.9,7500)
finalFrame.to_pickle("stockParetaData0425.pk1")
bestSelection.to_pickle("bestPick0425.pk1")
# bidAskChart = yd.getDetailedQuote('DOW')