# wolvesofDKSt  
Financial analysis of selling options for optimal risk/reward determination  
Final project for ME369P  
Nick Piacente, Ziam Ghaznavi, David Cayll  

## Project Summary: 

* Tool to collect and analyze stock market data.
* User interacts with a GUI to input specific investment details (risk, budget)
* The potential highest yielding option at a particular level of risk is highlighted
* Other possibilities are presented to show additional risk/reward information
* Specific financial instruments analyzed are Put options

## Packages Needed: 

yahoo_fin   
pandas   
mplcursors       
requests  
matplotlib  
numpy  
scipy        
tkinter  
datetime    

pip install --user yahoo-fin pandas mplcursors requests matplotlib numpy scipy datetime tkinter

## Getting Started:

1. Run **main.py**  
2. Enter two inputs:  
    - Probability of profit - Likeyhood of a profitable trade (level of risk)  
    - Budget - Amount of money that you want to put at risk  
3. Press Enter. Wait till data fetching and processing is complete.    
4. Results will be shown in the pop-up window once processing is complete 

## Included Files:  

### getYahooData.py

- File which includes methods used process data from yahoofinance.com
- main program should import this file to call the methods

Available methods:

getOptionsData(personalRiskTolerance, budget, printOutput = 'True')  
    return stockPareto, bestPick
    
getDetailedQuote(stock, ax1 = None)  
    return stockOptions
    
### main.py

- Creates a GUI window for user inputs 
- Creates a separate GUI with a plot of risk/reward for options in the users budget, bid/ask spread for selected option, and text information on the optimum option 

Methods:

startMainGUI():  
    return _root
    
gui_input(prompt1, prompt2):  
    return value1, value2
    
createParetoFig(_pareto_df,_bestPick):  
    return pareto_fig, pareto_ax
    
createDetailFig():  
    return detail_fig, detail_ax
    
drawBestData(_detail_fig, _detail_ax, _bestPick):  
    return _detail_fig
    
textOutput(_root, _Risk, _Budget, _bestPick):  
    return _textFrame
    
## Troubleshooting:

* Internet Connectivity
    * Make sure the internet is connected in order to fetch live data
    * Program data is most accurate during stock market hours (8:30 CST - 3:00 CST). This is when stock prices are active
    * Some glitches notices outside of market hours and at the beginning of the day, when prices are not live on yahoo finance (20 minute delay in pricing due to free data provided online)

* Spyder
    * Some bugs seen when using TKinter on mac machines using spyder
    * Best to run program in the command line

* inputs
    * Based on changing market conditions, there are situations when the user may enter inputs where no options are within the price range or risk level
    * Input dollar amounts must be above a certain threshold
    * It is best to stick inside the recommendations at the input prompt ($2000, no POP level higher than 90%)
    
## Comments:

Please reach out for any additional questions!
