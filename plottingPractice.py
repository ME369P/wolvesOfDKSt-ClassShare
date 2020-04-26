import numpy as np
import tkinter
import pandas as pd

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.cm as cm

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
matplotlib.use("TkAgg")
matplotlib.use("TkAgg")




import getYahooData as yd




# def plotOptions(ax, pareto_df, param_dict):
#     """
#     Function to plot options data from yahoo_fin

#     Parameters
#     ----------
#     ax : Axes
#     The axes to draw to

#     data1 : array
#         The x data

#     data2 : array
#         The y data

#     param_dict : dict
#         Dictionary of kwargs to pass to ax.plot

#     Returns
#     -------
#     out : list
#         list of artists added

#     """
#     tickerGroup = []
#     for ticker in pareto_df['Stock Name'].unique():
#         tickerGroup.append(pareto_df[pareto_df['Stock Name'] == ticker])
    
#     colors = cm.rainbow(np.linspace(0, 1, len(tickerGroup)))
#     for DF, c in zip(tickerGroup, colors):
#         out = DF.plot(kind='line',x='POP',y='Potential Gain Multiple Contracts', 
#                       legend = 'Stock Name', ax=ax, color=c)
#     return ax


class plotOptions(tkinter.Tk):
    
    Risk_num = 0
    Budget_num = 0
    startFlag = False
    
    def __init__(self, df, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Put Option Strategy")
        self.geometry('1500x800+100+100')
        # self._setup_inputGUI()
        # self._setup_gui()
        # self._questions = questions[:]
        # self._answers = answers
        # self._show_next_question()
    
    # def store_data():
    #     print("Risk: %s\nBudget: %s" % (Risk.get(), Budget.get()))
    #     Risk_num = float(Risk.get())
    #     Budget_num = float(Budget.get())
    #     return Risk_num, Budget_num
    
    def _setup_inputGUI(self):
        # risk level input
        self.tkinter.Label(textFrame, text="Risk Level").grid(row=1, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
        Risk = tkinter.Entry(textFrame)
        Risk.grid(row=1, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
        # budget level input
        self.Label(textFrame, text="Budget").grid(row=2, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
        Budget = tkinter.Entry(textFrame)
        Budget.grid(row=2, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
        self.Risk_num = Risk.get()
        self.Budget_num = Budget.get()
        go = tkinter.Button(textFrame, text='Enter')#, command=store_data)
        go.grid(row=3, column=1, columnspan=2)
    
    
    def startGUI(root):
        # initialize TK GUI window

        
        # input_root = tkinter.Tk()
        # input_root = tkinter.Toplevel()
        # input_root.wm_title("Inputs")
        textFrame = tkinter.Frame(root, relief = tkinter.RAISED, borderwidth=5)
        textFrame.pack()
        return textFrame
    
    
    
    ###########################################
    ############# Get Inputs ##################
    ###########################################
    
    def store_data(Risk_num, Budget_num):
        print("Risk: %s\nBudget: %s" % (Risk_num, Budget_num))
        startFlag = True
        return True
    
    def GetInputs(textFrame):
        tkinter.Label(textFrame, text="Risk Level").grid(row=1, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
        Risk = tkinter.Entry(textFrame)
        Risk.grid(row=1, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
        tkinter.Label(textFrame, text="Budget").grid(row=2, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
        Budget = tkinter.Entry(textFrame)
        Budget.grid(row=2, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
        Risk_num = Risk.get()
        Budget_num = Budget.get()
        go = tkinter.Button(textFrame, text='Enter', command=plotOptions.store_data(Risk_num, Budget_num))
        go.grid(row=3, column=1, columnspan=2)
        
        return Risk_num, Budget_num
    

    
    
    # T = tkinter.Text(root, height=2, width=30)
    # T.pack()
    # T.insert(tkinter.END, Risk_num)
    
    
    
    ############################################
    ######### Import data and Plot #############
    ############################################
    def printDetailFig(self, BestTicker):
        # initialize figure and axes objects using pyplot for detail plot
        detail_fig = plt.figure(figsize= (6,4), dpi = 100)
        detail_ax = detail_fig.add_subplot(111)
        yd.getDetailedQuote('DOW', detail_ax)
        # put detail axes into tkinter GUI 
        canvas = FigureCanvasTkAgg(detail_fig, master=root)
        canvas.get_tk_widget().pack(side=tkinter.LEFT, anchor=tkinter.NW)#, fill=tkinter.X)#, expand=1)
        
    
    
    def printParetoCurve(self):
        # initalize figure and axes objects using pyplot for pareto curve
        pareto_fig = plt.figure(figsize=(8,7), dpi=100)
        pareto_ax = pareto_fig.add_subplot(111)
        # stockPareto, bestPick = yd.getOptionsData(0.9, 10000)
        stockPareto = pd.read_pickle('stockParetaData0425.pk1')
        stockPareto.plot(kind='scatter',x='POP',y='Potential Gain Multiple Contracts', legend = 'Stock Name', ax = pareto_ax)
        pareto_ax.set_title('Pareto Curve for Best Options (Puts)')
        pareto_ax.set_xlabel('Probability of Profit (%)')
        pareto_ax.set_ylabel('Premium Collected')
        
        
        # put pareto curve axes into tkinter GUI
        canvas = FigureCanvasTkAgg(pareto_fig, master=root)
        canvas.get_tk_widget().pack(side=tkinter.RIGHT, anchor=tkinter.NE)#, fill=tkinter.Y)#, expand=1)
    
    
    # canvas.create_oval(10, 10, 80, 80, outline="#f11",fill="#1f1", width=2)
    
    
    
    
    
    
    
    
    # # plot data to respective axes objects
    # # pareto_ax.plot(t, s)
    
    
    # ##
    
    
    
    
    
    # # adds in toolbar for paretoCurve plot
    # toolbar = NavigationToolbar2Tk(canvas, root)
    # toolbar.update()
    # canvas._tkcanvas.pack(side=tkinter.LEFT)#, fill=tkinter.BOTH, expand=1)
    
    
    def callback():
        print("click!")
    
    
    
    def refresh():
        print("refresh")
    
    # b = tkinter.Button(master=root, text="Quit", command=callback)
    # b.pack(side=tkinter.LEFT, anchor=tkinter.SW)
    # refresh = tkinter.Button(master=root, text = "Refresh", command=refresh)
    # refresh.pack(side=tkinter.LEFT, anchor=tkinter.SW)
    
    



if __name__ == '__main__':
    print('main')
    # textFrame, root = startGUI()
    # Risk_num, Budget_num = GetInputs(textFrame)
    # stored = store_data()
    # print(stored)
    
    stockPareto = pd.read_pickle('stockParetaData0425.pk1')
    root = plotOptions(stockPareto)
    textFrame = plotOptions.startGUI(root)
    
    tkinter.Label(textFrame, text="Risk Level").grid(row=1, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
    Risk = tkinter.Entry(textFrame)
    Risk.grid(row=1, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
    tkinter.Label(textFrame, text="Budget").grid(row=2, column=1)#side=tkinter.LEFT, anchor=tkinter.SW)
    Budget = tkinter.Entry(textFrame)
    Budget.grid(row=2, column=2)#side=tkinter.LEFT, anchor=tkinter.SW)
    Risk_num = Risk.get()
    Budget_num = Budget.get()
    go = tkinter.Button(textFrame, text='Enter', command=plotOptions.store_data(Risk_num, Budget_num))
    go.grid(row=3, column=1, columnspan=2)
    # Risk, Budget = plotOptions.GetInputs(textFrame)
    
    

    #getOptionsData(personalRiskTolerance, budget, printOutput = False)
    # charty = getDetailedQuote('DOW', ax)
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



# def create_widgets(self):
#     self.hi_there = tkinter.Button(self)
#     self.hi_there["text"] = "Hello World\n(click me)"
#     self.hi_there["command"] = self.say_hi
#     self.hi_there.pack(side="left")

#     self.quit = tkinter.Button(self, text="QUIT", fg="red",
#                           command=self.master.destroy)
#     self.quit.pack(side="bottom")