import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
# Tkinter is for python 2; tkinter is for python 3
if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkMessageBox, tkFileDialog

else:
    import tkinter as tk
    from tkinter import messagebox as tkMessageBox
    from tkinter import filedialog as tkFileDialog

class MainApp(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title('App')
        # call the widgets
        self.okButton()
        self.quitButton()
        self.readDataButton()
        self.clearDataButton()
        self.velScale()
        self.canvas()

    # print messages on the screen
    def printMessage(self):
        if (self.data):
            print("Data is loaded and accessible from here (printMessage()).")
        else:
            print('No data loaded...')

    ### OK button
    def okButton(self):
        self.okButton = tk.Button(self, text='Test', command=self.printMessage)
        self.okButton.grid(column=1, row=1, sticky="nesw")

    ### Quit button
    def quitButton(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.confirmQuit)
        self.quitButton.grid(column=1, row=2, sticky="nesw")
    # confirm quitting
    def confirmQuit(self):
        answer = tkMessageBox.askyesno(title="App", message="Do you really want to quit?")
        if (answer):
            self.quit()

    # Read data button
    def readDataButton(self):
        self.data = None
        self.readDataButton = tk.Button(self, text='Import data', command=self.readData)
        self.readDataButton.grid(column=1, row=3, sticky="nesw")
    # reading data
    def readData(self):
        import os
        fullPath = dataList = tkFileDialog.askopenfilename(initialdir='path/to/initialdir')
        dataDir = os.path.split(fullPath)[0]+'/'
        self.data = readData(fullPath)

    # Clear data from current session
    def clearDataButton(self):
        self.clearData = tk.Button(self, text='Clear data', command=self.confirmClearData)
        self.clearData.grid(column=1, row=4, sticky="nesw")
    # confirm clearing data
    def confirmClearData(self):
        answer = tkMessageBox.askyesno(title="App", message="Are you sure you want to clear the loaded data?")
        if (answer):
            self.data = None
            tkMessageBox.showwarning(title="App", message="Data has been deleted.")

    # Velocity scale
    def velScale(self):
        self.velVar = tk.StringVar()
        velLabel = tk.Label(self, text="Scale value:", textvariable=self.velVar)
        velLabel.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E)
        velScale = tk.Scale(self, from_=-500, to=+500, orient=tk.HORIZONTAL, resolution=20,
                        sliderlength=20, showvalue=0,
                        length=200, width=20,
                        command=self.onVelScale)
        velScale.grid(column=1, row=5, sticky="nesw")
    # update velLabel
    def onVelScale(self, val):
        self.velVar.set("Scale value: {:+0.0f}".format(float(val)))

    # Canvas
    def canvas(self):
        self.f = Figure(figsize=(4,2))
        self.a = self.f.add_subplot(111)
        self.a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.get_tk_widget().grid(column=2, row=1, rowspan=5, sticky="nesw")

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.parent)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600+10+10")
    root.resizable(0, 0)
    MainApp(root).pack(side=tk.TOP)
    root.mainloop()