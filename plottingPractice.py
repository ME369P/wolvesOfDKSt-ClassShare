import numpy as np
import tkinter
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
matplotlib.use("TkAgg")


# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.cm as cm
import getYahooData as yd


# convert pandas dataframe into a np array
# a = pandas.DataFrame(np.random.rand(4,5), columns = list('abcde'))
# a_asndarray = a.values

def plotOptions(ax, pareto_df, param_dict):
    """
    Function to plot options data from yahoo_fin

    Parameters
    ----------
    ax : Axes
    The axes to draw to

    data1 : array
        The x data

    data2 : array
        The y data

    param_dict : dict
        Dictionary of kwargs to pass to ax.plot

    Returns
    -------
    out : list
        list of artists added

    """
    tickerGroup = []
    for ticker in pareto_df['Stock Name'].unique():
        tickerGroup.append(pareto_df[pareto_df['Stock Name'] == ticker])
    
    colors = cm.rainbow(np.linspace(0, 1, len(tickerGroup)))
    for DF, c in zip(tickerGroup, colors):
        out = DF.plot(kind='line',x='POP',y='Potential Gain Multiple Contracts', 
                      legend = 'Stock Name', ax=ax, color=c)
    return ax



# def create_widgets(self):
#     self.hi_there = tkinter.Button(self)
#     self.hi_there["text"] = "Hello World\n(click me)"
#     self.hi_there["command"] = self.say_hi
#     self.hi_there.pack(side="left")

#     self.quit = tkinter.Button(self, text="QUIT", fg="red",
#                           command=self.master.destroy)
#     self.quit.pack(side="bottom")


def store_data():
    print("Risk: %s\nBudget: %s" % (Risk.get(), Budget.get()))
    Risk_num = float(Risk.get())
    Budget_num = float(Budget.get())
    return Risk_num, Budget_num


# initialize TK GUI window
root = tkinter.Tk()
root.wm_title("Put Option Strategy")
root.geometry('1500x800+100+100')

input_root = tkinter.Tk()
input_root = tkinter.Toplevel()
input_root.wm_title("Inputs")
textFrame = tkinter.Frame(input_root, relief = tkinter.RAISED, borderwidth=5)
textFrame.pack()



###########################################
############# Get Inputs ##################
###########################################

tkinter.Label(textFrame, text="Risk Level").pack()#side=tkinter.LEFT, anchor=tkinter.SW)
Risk = tkinter.Entry(textFrame)
Risk.pack()#side=tkinter.LEFT, anchor=tkinter.SW)
tkinter.Label(textFrame, text="Budget").pack()#side=tkinter.LEFT, anchor=tkinter.SW)
Budget = tkinter.Entry(textFrame)
Budget.pack()#side=tkinter.LEFT, anchor=tkinter.SW)
Risk_num = Risk.get()
Budget_num = Budget.get()

    
tkinter.Button(textFrame, text='Enter', command=store_data).pack()



############################################
######### Import data and Plot #############
############################################

# initialize figure and axes objects using pyplot for detail plot
detail_fig = plt.figure(figsize= (6,4), dpi = 100)
detail_ax = detail_fig.add_subplot(111)
yd.getDetailedQuote('DOW', detail_ax)
# put detail axes into tkinter GUI 
canvas = FigureCanvasTkAgg(detail_fig, master=root)
canvas.get_tk_widget().pack(side=tkinter.LEFT, anchor=tkinter.NW)#, fill=tkinter.X)#, expand=1)


# initalize figure and axes objects using pyplot for pareto curve
pareto_fig = plt.Figure(figsize=(8,7), dpi=100)
pareto_ax = pareto_fig.add_subplot(111)
pareto_ax.set_title('Pareto Curve for Best Options (Puts)')
pareto_ax.set_xlabel('Probability of Profit (%)')
pareto_ax.set_ylabel('Premium Collected')
# stockPareto, bestPick, stockParetoChart = yd.getOptionsData(0.9, 100000, pareto_ax)
# put pareto curve axes into tkinter GUI
canvas = FigureCanvasTkAgg(pareto_fig, master=root)
canvas.get_tk_widget().pack(side=tkinter.RIGHT, anchor=tkinter.NE)#, fill=tkinter.Y)#, expand=1)








# # plot data to respective axes objects
# # pareto_ax.plot(t, s)


# ##





# # adds in toolbar for paretoCurve plot
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas._tkcanvas.pack(side=tkinter.LEFT)#, fill=tkinter.BOTH, expand=1)


def callback():
    print("click!")

b = tkinter.Button(master=root, text="Quit", command=callback)
b.pack(side=tkinter.LEFT, anchor=tkinter.SW)

def refresh():
    print("refresh")

refresh = tkinter.Button(master=root, text = "Refresh", command=refresh)
refresh.pack(side=tkinter.LEFT, anchor=tkinter.SW)

tkinter.mainloop()






















# class Application(tkinter.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.pack()
#         self.create_widgets()

#     def create_widgets(self):
#         self.hi_there = tkinter.Button(self)
#         self.hi_there["text"] = "Hello World\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")

#         self.quit = tkinter.Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         self.quit.pack(side="bottom")

#     def say_hi(self):
#         print("hi there, everyone!")