import numpy as np
import tkinter
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.cm as cm



# convert pandas dataframe into a np array
# a = pandas.DataFrame(np.random.rand(4,5), columns = list('abcde'))
# a_asndarray = a.values

def plotOptions(ax, list_DF, param_dict):
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
    colors = cm.rainbow(np.linspace(0, 1, len(list_DF)))
    for DF, c in zip(list_DF, colors):
        out = DF.plot(kind='scatter',x='POP',y='Potential Gain Multiple Contracts', legend = 'Stock Name', ax=ax, color=c)
    return out
    plt.axes(ax)

def create_widgets(self):
    self.hi_there = tkinter.Button(self)
    self.hi_there["text"] = "Hello World\n(click me)"
    self.hi_there["command"] = self.say_hi
    self.hi_there.pack(side="left")

    self.quit = tkinter.Button(self, text="QUIT", fg="red",
                          command=self.master.destroy)
    self.quit.pack(side="bottom")


root = tkinter.Tk()
root.wm_title("Put Option Strategy")
root.geometry('1500x800+100+100')
fig = Figure(figsize=(9,8), dpi=100)
ax = fig.add_subplot(111)
t = np.arange(0.0, 3.0, 0.01)
s = np.sin(2*np.pi*t)
ax.plot(t,s)
# plotOptions(ax, , {})


# ax.plot(t, s)
ax.set_title('Pareto Curve for Best Options (Puts)')
ax.set_xlabel('Probability of Profit (%)')
ax.set_ylabel('Premium Collected')

##




# a tk.DrawingArea
canvas = FigureCanvasTkAgg(fig, master=root)

canvas.get_tk_widget().pack(side=tkinter.RIGHT)#, fill=tkinter.Y)#, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=tkinter.RIGHT)#, fill=tkinter.BOTH, expand=1)


def callback():
    print("click!")

b = tkinter.Button(master=root, text="OK", command=callback)
b.pack(side=tkinter.BOTTOM)

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