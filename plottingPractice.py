import numpy as np
import tkinter
import pandas as pd
import mplcursors

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.cm as cm

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
matplotlib.use("TkAgg")

import getYahooData as yd

plt.ion()

    
Risk_num = 0
Budget_num = 0



def startMainGUI():
    _root = tkinter.Tk()
    _root.title("Put Option Strategy")
    _root.geometry('1500x800+100+100')
    return _root



###########################################
############# Get Inputs ##################
###########################################


def GetInputs(_textFrame):
    tkinter.Label(_textFrame, text="Risk Level").grid(row=1, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
    Risk = tkinter.Entry(_textFrame)
    Risk.grid(row=1, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
    tkinter.Label(_textFrame, text="Budget").grid(row=2, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
    Budget = tkinter.Entry(_textFrame)
    Budget.grid(row=2, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
    Risk_num = Risk.get()
    Budget_num = Budget.get()
    go = tkinter.Button(_textFrame, text='Enter', command=store_data(Risk_num, Budget_num, _textFrame))
    go.grid(row=3, column=1, columnspan=2)
    
    return Risk_num, Budget_num






############################################
######### Import data and Plot #############
############################################



def gui_input(prompt1, prompt2):

    _root = tkinter.Tk()
    _root.title("User Details")
    # _root.geometry('1500x800+100+100')
    # this will contain the entered string, and will
    # still exist after the window is destroyed
    var1 = tkinter.StringVar()
    var2 = tkinter.StringVar()

    # create the GUI
    label1 = tkinter.Label(_root, text=prompt1)
    entry1 = tkinter.Entry(_root, textvariable=var1)
    label1.grid(row=1, column=1)
    entry1.grid(row=1, column=2)
    
    label2 = tkinter.Label(_root, text=prompt2)
    entry2 = tkinter.Entry(_root, textvariable=var2)
    label2.grid(row=2, column=1)
    entry2.grid(row=2, column=2)
    
    go = tkinter.Button(_root, text='Enter')#, command=store_data)
    go.grid(row=3, column=1, columnspan=2)

    # Let the user press the return key to destroy the gui 
    go.bind("<Button-1>", lambda event: _root.destroy())

    # this will block until the window is destroyed
    _root.mainloop()

    # after the window has been destroyed, we can't access
    # the entry widget, but we _can_ access the associated
    # variable
    value1 = var1.get()
    value2 = var2.get()
    return value1, value2

def createParetoFig(_pareto_df):
    # initalize figure and axes objects using pyplot for pareto curve
    pareto_fig = Figure(figsize=(8,7.5), dpi=100)
    pareto_ax = pareto_fig.add_subplot(111)
    pareto_ax.set_title('Pareto Curve for Best Options (Puts)')
    pareto_ax.set_xlabel('Probability of Profit (%)')
    pareto_ax.set_ylabel('Premium Collected')
    _pareto_df.plot.scatter(x='POP',y='Potential Gain Multiple Contracts', ax = pareto_ax)
    # ax = finalFrame.plot(kind = 'scatter', x='POP',y='Potential Gain Multiple Contracts')

    
    # pareto_ax.legend()
    # stockPareto, bestPick, stockParetoChart = yd.getOptionsData(0.9, 100000, pareto_ax)
    # put pareto curve axes into tkinter GUI
    # canvas = FigureCanvasTkAgg(pareto_fig, master=root)
    # canvas.get_tk_widget().grid(row=1, column=2, rowspan=2)#pack(side=tkinter.RIGHT, anchor=tkinter.NE)#, fill=tkinter.Y)#, expand=1)
    return pareto_fig, pareto_ax

def plotPareto(_pareto_ax, _pareto_df):
    """
    plots the data in "_pareto_df" to _pareto_ax grouped by ticker and color coded
    """
    
    # show contract name
    # _pareto_ax = _pareto_df.plot.scatter(x='POP',y='Potential Gain Multiple Contracts')
    # # ax = finalFrame.plot(kind = 'scatter', x='POP',y='Potential Gain Multiple Contracts')
    # mplcursors.cursor(hover=True).connect(
    #     "add", lambda sel: sel.annotation.set_text(_pareto_df.index[sel.target.index]))


    
    # _tickerGroup = []
    # dct = dict()
    # i = 0
    # # makes a list of dataframes with common stock names. 
    # for ticker in _pareto_df['Stock Name'].unique():
    #     _tickerGroup.append(_pareto_df[_pareto_df['Stock Name'] == ticker])
        
    # colors = [tuple(l) for l in cm.rainbow(np.linspace(0, 1, len(_tickerGroup)))] # unique color for each option series
    
    # # creates a dictionary in form of {stock name: tuple(['POP'], ['Gain'])}
    # for DF, c in zip(_tickerGroup, colors):
    #     dct[_pareto_df['Stock Name'].unique()[i]]= (DF['POP'].tolist(), DF['Potential Gain Multiple Contracts'].tolist())
    #     i+=1
        
    # # prints each dataseries and use dictionary key as label for creating legend
    # for i,c in zip(dct, colors):
    #     _pareto_ax.plot(*dct[i], label=i, color = c, marker='*', linestyle='None')
        
        
    # _pareto_ax.legend()


def createDetailFig():
    # initalize figure and axes objects using pyplot for pareto curve
    detail_fig = Figure(figsize=(7.50,4.00), dpi=100)
    detail_ax = detail_fig.add_subplot(111)

    # pareto_ax.legend()
    # stockPareto, bestPick, stockParetoChart = yd.getOptionsData(0.9, 100000, pareto_ax)
    # put pareto curve axes into tkinter GUI
    # canvas = FigureCanvasTkAgg(pareto_fig, master=root)
    # canvas.get_tk_widget().grid(row=1, column=2, rowspan=2)#pack(side=tkinter.RIGHT, anchor=tkinter.NE)#, fill=tkinter.Y)#, expand=1)
    return detail_fig, detail_ax


def drawBestData(_detail_fig, _detail_ax, _bestPick):
    yd.getDetailedQuote(_bestPick, _detail_ax)
    _detail_fig.axes.append(_detail_ax)
    return _detail_fig

def textOutput(_root, _Risk, _Budget, _bestPick):
    _textFrame = tkinter.Frame(_root, relief = tkinter.RAISED, borderwidth=5)
    # print out risk and budget levels
    label1 = tkinter.Label(_textFrame, text="Risk is: {}%".format(float(_Risk)*100))
    label1.grid(row=1, column=1)
    label2 = tkinter.Label(_textFrame, text="Budget is: ${}".format(Budget))
    label2.grid(row=2, column=1)
    
    # print out winning option information
    label3 = tkinter.Label(_textFrame, text = "Contract Name: {}".format(_bestPick.name))
    label3.grid(row=3, column=1)
    label4 = tkinter.Label(_textFrame, text = "Probability of Profit: {}".format(_bestPick['POP']))
    label4.grid(row=4, column=1)
    label5 = tkinter.Label(_textFrame, text = "Potential Gain: {}".format(_bestPick['Potential Gain Multiple Contracts']))
    label5.grid(row=5, column=1)
    label6 = tkinter.Label(_textFrame, text = "Number of Contracts: {}".format(_bestPick['contractsInBudget']))
    label6.grid(row=6, column=1)
    return _textFrame


if __name__ == '__main__':
    print('main')
    
    # create window to ask for user inputs
    Risk, Budget = gui_input("Enter your desired risk:", "Enter your available budget:")
    print("risk: {} budget: {}".format(Risk, Budget))
    
    # create main window and configure grid size
    root = startMainGUI()
    root.grid_columnconfigure(1,minsize=750)
    root.grid_rowconfigure(1,minsize=400)
    root.grid_columnconfigure(2,minsize=750)
    root.grid_rowconfigure(2,minsize=400)
    
    # get stockPareto data from yd
    stockPareto, bestPick = yd.getOptionsData(float(Risk), float(Budget))
    # stockPareto = pd.read_pickle('stockParetaData0425.pk1')
    # bestPick = pd.read_pickle('bestPick0425.pk1')
    
    # create figure and axes objects for stockPareto to be placed into 
    pareto_fig, pareto_ax = createParetoFig(stockPareto)
    
    #place stockPareto data into the axes created above
    # plotPareto(pareto_ax, stockPareto)
    canvas = FigureCanvasTkAgg(pareto_fig, master=root)
    
    # add cursor 
    mplcursors.cursor(pareto_ax, hover=True).connect(
        "add", lambda sel: sel.annotation.set_text(stockPareto.index[sel.target.index]))
    canvas.get_tk_widget().grid(row=1, column=1, rowspan=2)
    
    # create figure and axes objects for detail plot to be placed into 
    detail_fig, detail_ax = createDetailFig()
    
    # place bestPick figure into detail_fig
    detail_fig = drawBestData(detail_fig, detail_ax, bestPick['Stock Name'])
    canvas = FigureCanvasTkAgg(detail_fig, master=root)
    canvas.get_tk_widget().grid(row=1, column=2)#, rowspan=2)
    
    # create text frame
    testFrame = textOutput(root, Risk, Budget, bestPick)
    testFrame.grid(row=2, column=2, sticky = "NESW")
    # canvas.get_tk_widget()

    
    # # initalize figure and axes objects using pyplot for pareto curve
    # pareto_fig = plt.Figure(figsize=(8,7), dpi=100)
    # pareto_ax = pareto_fig.add_subplot(111)
    # pareto_ax.set_title('Pareto Curve for Best Options (Puts)')
    # pareto_ax.set_xlabel('Probability of Profit (%)')
    # pareto_ax.set_ylabel('Premium Collected')
    # # stockPareto, bestPick, stockParetoChart = yd.getOptionsData(0.9, 100000, pareto_ax)
    # # put pareto curve axes into tkinter GUI
    # canvas = FigureCanvasTkAgg(pareto_fig, master=root)
    # canvas.get_tk_widget().pack(side=tkinter.RIGHT, anchor=tkinter.NE)#, fill=tkinter.Y)#, expand=1)
    
    
    
    
    
    
    # tkinter.Label(textFrame, text="Risk Level").grid(row=1, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
    # Risk = tkinter.Entry(textFrame)
    # Risk.grid(row=1, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
    # tkinter.Label(textFrame, text="Budget").grid(row=2, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
    # Budget = tkinter.Entry(textFrame)
    # Budget.grid(row=2, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
    # Risk_num = Risk.get()
    # Budget_num = Budget.get()
    # go = tkinter.Button(textFrame, text='Enter', command=plotOptions.store_data(Risk_num, Budget_num, textFrame))
    # go.grid(row=3, column=1, columnspan=2)
    # # Risk, Budget = plotOptions.GetInputs(textFrame)
    
    
    
    #getOptionsData(personalRiskTolerance, budget, printOutput = False)
    # charty = getDetailedQuote('DOW', ax)
    tkinter.mainloop()






