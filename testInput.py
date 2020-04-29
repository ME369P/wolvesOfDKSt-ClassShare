# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:28:57 2020

@author: -
"""
import tkinter

def gui_input(prompt1, prompt2):

    _root = tkinter.Tk()
    _root.title('Wolves of DK St - Options Strategy Visualization')
    _root.geometry("+1200+800")
    # _root.geometry('1500x800+100+100')
    # this will contain the entered string, and will
    # still exist after the window is destroyed
    var1 = tkinter.StringVar()
    var2 = tkinter.StringVar()

    # Starting Message
    
    tkinter.Label(_root, text='Welcome to the Options Strategy Visualization').grid(row=1, column=1, columnspan=2)
    tkinter.Label(_root, text='Enter your appropriate risk level:').grid(row=3, column=1, columnspan=2)
    tkinter.Label(_root, text=' ').grid(row=2, column=1, columnspan=2)
    tkinter.Label(_root, text='0.1 = 10% chance of profit (Throw your money away)').grid(row=4, column=1, columnspan=2)
    tkinter.Label(_root, text='0.5 = 50% chance of profit (gambling)').grid(row=5, column=1, columnspan=2)
    tkinter.Label(_root, text='0.9 = 90% chance of profit (high chance for profit)').grid(row=6, column=1, columnspan=2)
    tkinter.Label(_root, text=' ').grid(row=7, column=1, columnspan=2)
    tkinter.Label(_root, text=' ').grid(row=8, column=1, columnspan=2)
    # create the GUI
    label1 = tkinter.Label(_root, text=prompt1)
    entry1 = tkinter.Entry(_root, textvariable=var1)
    label1.grid(row=9, column=1)
    entry1.grid(row=9, column=2)
    
    label2 = tkinter.Label(_root, text=prompt2)
    entry2 = tkinter.Entry(_root, textvariable=var2)
    label2.grid(row=10, column=1)
    entry2.grid(row=10, column=2)
    
    go = tkinter.Button(_root, text='Enter')#, command=store_data)
    go.grid(row=11, column=1, columnspan=2)

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

Risk, Budget = gui_input("Desired Risk:", "Available Budget:")
print("risk: {} budget: {}".format(Risk, Budget))