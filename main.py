# main.py
# Date Created: 4/19/20
# Date Last Modified: 04/30/20
# By: David Cayll and Nick Piacente and Ziam Ghaznavi

# Functions for generating figures and tkinter windows and frames

import numpy as np
import tkinter
import pandas as pd
import mplcursors
# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
matplotlib.use("TkAgg")
import getYahooData as yd
plt.ion()



def startMainGUI():
    """
    Create main GUI window

    Returns
    -------
    _root : tkinter window object
        DESCRIPTION.

    """
    _root = tkinter.Tk()
    _root.title("Wolves of DK - Option Strategy Visualization")
    _root.geometry('1200x700+100+100')
    return _root



###########################################
############# Get Inputs ##################
###########################################

def gui_input(prompt1, prompt2):
    """
    Creates a window to collect Risk and Budget info from user

    Parameters
    ----------
    prompt1 : String
        First question in input prompt
    prompt2 : String
        Second question in input prompt

    Returns
    -------
    value1 : String
        Value of response to the question asked in prompt1
    value2 : String
        Value of response to the question asked in prompt2

    """
    
    # create tkinterwindow and set title and geometry of window
    _root = tkinter.Tk()
    _root.title('Wolves of DK St - Options Strategy Visualization')
    _root.geometry("+600+400")

    # Set text for input screen
    tkinter.Label(_root, text='Welcome to the Options Strategy Visualization').grid(row=1, column=1, columnspan=2)
    tkinter.Label(_root, text='Enter your desired probability of profit:').grid(row=3, column=1, columnspan=2)
    tkinter.Label(_root, text=' ').grid(row=2, column=1, columnspan=2)
    tkinter.Label(_root, text='0.1 = 10% chance of profit (Throw your money away)').grid(row=4, column=1, columnspan=2)
    tkinter.Label(_root, text='0.5 = 50% chance of profit (gambling)').grid(row=5, column=1, columnspan=2)
    tkinter.Label(_root, text='0.9 = 90% chance of profit (high chance for profit)').grid(row=6, column=1, columnspan=2)
    tkinter.Label(_root, text=' ').grid(row=8, column=1, columnspan=2)
    tkinter.Label(_root, text='Enter your desired budget (number, min $2000)').grid(row=9, column=1, columnspan=2)
    tkinter.Label(_root, text='Please enter only numeric digits, no characters').grid(row=10, column=1, columnspan=2)
    tkinter.Label(_root, text=' ').grid(row=13, column=1, columnspan=2)
    
    # set prompt and input text; setup input collection to be saved to var1 and var2
    var1 = tkinter.StringVar()
    var2 = tkinter.StringVar()
    label1 = tkinter.Label(_root, text=prompt1)
    entry1 = tkinter.Entry(_root, textvariable=var1)
    label1.grid(row=7, column=1)
    entry1.grid(row=7, column=2)
    
    label2 = tkinter.Label(_root, text=prompt2)
    entry2 = tkinter.Entry(_root, textvariable=var2)
    label2.grid(row=12, column=1)
    entry2.grid(row=12, column=2)
    
    # create an "Enter" button to conclude data collection and exit GUI
    go = tkinter.Button(_root, text='Enter')#, command=store_data)
    go.grid(row=14, column=1, columnspan=2)
    go.bind("<Button-1>", lambda event: _root.destroy())

    # this will block main method from advancing until the window is destroyed
    _root.mainloop()

    # after the window has been destroyed, we can't access
    # the entry widget, but we _can_ access the associated
    # variable
    value1 = var1.get()
    value2 = var2.get()
    
    return value1, value2



###################################################
######### Import data and Plot Pareto #############
###################################################

def createParetoFig(_pareto_df,_bestPick):
    """
    Initalize figure and axes objects using pyplot for pareto curve

    Parameters
    ----------
    _pareto_df : Pandas DataFrame
        DataFrame from Yahoo_fin that contains all the relevant options data
    _bestPick : Pandas Series
        Option data for the best pick given the user input settings

    Returns
    -------
    pareto_fig : matplotlib figure object
        figure used to plot the stockPareto data from the _pareto_df input
    pareto_ax : matplotlib axes object
        axes object that holds the stockPareto data from _pareto_df input
        plotted using pandas integrated matplotlib .plot function

    """
    
    pareto_fig = Figure(figsize=(6,6), dpi=100)
    pareto_ax = pareto_fig.add_subplot(111)
    pareto_ax.set_title('Pareto Curve of Available Options in DOW JONES Index')
    _pareto_df.plot.scatter(x='POP',y='Potential Gain Multiple Contracts', ax = pareto_ax)
    pareto_ax.set_xlabel('Probability of Profit (%)')
    pareto_ax.set_ylabel('Potential Gain ($)')
    # ax = finalFrame.plot(kind = 'scatter', x='POP',y='Potential Gain Multiple Contracts')
    pareto_ax.axvline(_bestPick['POP'], color='green', ls='--')
    pareto_ax.axhline(_bestPick['Potential Gain Multiple Contracts'], color='green', ls='--')
    
    return pareto_fig, pareto_ax



###############################################################################
######### Creating and plot figure / axes for bid/ask spread plot #############
###############################################################################

def createDetailFig():
    """
    Creating and plot figure / axes for bid/ask spread plot

    Returns
    -------
    detail_fig : matplotlib figure object
        figure used to plot the bidAskSpread data 
    detail_ax : matplotlib axes object
        axes object that will hold the bidAskSpread data

    """
    
    detail_fig = Figure(figsize=(6,6), dpi=100)
    detail_ax = detail_fig.add_subplot(111)

    return detail_fig, detail_ax


def drawBestData(_detail_fig, _detail_ax, _bestPick):
    """
    Draws the BidAsk Spread data from the _bestPick option into the _detail_fig figure object

    Parameters
    ----------
    _detail_fig : matplotlib figure
        figure used to plot the bidAskSpread data 
    _detail_ax : TYPE
        DESCRIPTION.
    _bestPick : matplotlib axes object
        axes object that holds the bidAskSpread data

    Returns
    -------
    _detail_fig : matplotlib figure
        figure with bidAskSpread data plotted graphically in the _detail_ax axes

    """
    
    xPoint = _bestPick['Strike']
    yPoint = _bestPick['Potential Gain']/100
    yd.getDetailedQuote(_bestPick['Stock Name'], _detail_ax)
    _detail_ax.plot(xPoint,yPoint,'ro')
    _detail_fig.axes.append(_detail_ax)
    return _detail_fig



##########################################################################
######### Print text to screen with contract details from DF #############
##########################################################################

def textOutput(_root, _Risk, _Budget, _bestPick):
    """
    Creates tkinter frame with relevant options data

    Parameters
    ----------
    _root : tkinter frame 
        frame used to plot text output to 
    _Risk : float
        user inputted risk decimal
    _Budget : float
        user inputted budget
    _bestPick : pandas Series
        Option data for the best pick given the user input settings

    Returns
    -------
    _textFrame : tkinter frame
        Frame with the formatted selected bestPick option data

    """
    # create a tkinter frame to print text to
    _textFrame = tkinter.Frame(_root, relief = tkinter.RAISED, borderwidth=5)
    
    # print out risk and budget levels
    label1 = tkinter.Label(_textFrame, padx = 10, borderwidth = 3, text="POP desired is: {}%".format((_Risk)*100))
    label1.grid(row=1, column=1)
    label2 = tkinter.Label(_textFrame, padx = 10, borderwidth = 3, text="Budget is: ${}".format(Budget))
    label2.grid(row=1, column=2)
    
    # print out winning option information
    label3 = tkinter.Label(_textFrame, padx = 10, borderwidth = 3, text = "Contract Name: {}".format(_bestPick.name))
    label3.grid(row=1, column=3)
    label4 = tkinter.Label(_textFrame, padx = 10, borderwidth = 3, text = "Probability of Profit: {:.2f}%".format(_bestPick['POP']))
    label4.grid(row=1, column=4)
    label5 = tkinter.Label(_textFrame, padx = 10, borderwidth = 3, text = "Potential Gain: ${:.2f}".format(_bestPick['Potential Gain Multiple Contracts']))
    label5.grid(row=1, column=5)
    label6 = tkinter.Label(_textFrame, padx = 10, borderwidth = 3, text = "Stock: {}".format(_bestPick['Stock Name']))
    label6.grid(row=1, column=6)
    label7 = tkinter.Label(_textFrame, text = "THIS IS NOT FINANCIAL ADVICE", font=("Courier", 16), fg="red")
    label7.grid(row=2, column=1, columnspan = 6)
    
    return _textFrame



####################################
######### Main Method  #############
####################################

if __name__ == '__main__':
    print('main')
    
    # create window to ask for user inputs
    Risk, Budget = gui_input("Desired probability of profit:", "Available budget:")
    Risk = float(Risk)
    Budget = float(Budget)
    print("Finding the best options contracts with a ${} budget and {}% probability of profit".format(Budget, ((Risk)*100)))
    
    # create main window and configure grid size
    root = startMainGUI()
    root.grid_columnconfigure(1,minsize=600)
    root.grid_rowconfigure(1,minsize=600)
    
    # get stockPareto data from yd
    stockPareto, bestPick = yd.getOptionsData(Risk, Budget)
    
    # create figure and axes objects for stockPareto to be placed into 
    pareto_fig, pareto_ax = createParetoFig(stockPareto, bestPick)
    
    #place pareto_fig into tkinter window
    canvas = FigureCanvasTkAgg(pareto_fig, master=root)
    # add cursor 
    mplcursors.cursor(pareto_ax, hover=True).connect(
        "add", lambda sel: sel.annotation.set_text(stockPareto['printString'][sel.target.index]))
    canvas.get_tk_widget().grid(row=1, column=1)
    
    # create figure and axes objects for detail plot to be placed into 
    detail_fig, detail_ax = createDetailFig()
    
    # place bestPick figure into detail_fig and print to tkinter window
    detail_fig = drawBestData(detail_fig, detail_ax, bestPick)
    canvas = FigureCanvasTkAgg(detail_fig, master=root)
    canvas.get_tk_widget().grid(row=1, column=2)
    
    # place textFrame into tkinter window
    testFrame = textOutput(root, Risk, Budget, bestPick)
    testFrame.grid(row=2, column=1, columnspan = 2)

    tkinter.mainloop()