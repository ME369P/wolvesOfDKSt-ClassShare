# pullOption.py
# Date Created: 4/11/20
# Date Last Modified: XX
# By: Nick Piacente

# get an option quote using yahoo_fin

from yahoo_fin import options
from yahoo_fin import stock_info

stock = 'AAPL'

aaplCallChain = options.get_calls(stock)
currentPrice=stock_info.get_live_price(stock)
info = stock_info.get_quote_table(stock)

aaplOptions = options.get_calls(stock).plot(x='Strike',y=['Bid','Ask'], xlim=[.5*currentPrice,1.5*currentPrice],title='Bid/Ask Call Spread for {}'.format(stock))
aaplOptions.axvline(currentPrice, color='green', ls='--')