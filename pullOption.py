# pullOption.py
# Date Created: 4/11/20
# Date Last Modified: XX
# By: Nick Piacente

# get an option quote using yahoo_fin

from yahoo_fin import options
from yahoo_fin import stock_info
import tkinter as tk
import numpy as np
from matplotlib.figure import Figure

import matplotlib as mpl
import sys

import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

from matplotlib.figure import Figure
from matplotlib.backends import _backend_tk


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    # tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
    _backend_tk.blit(photo, figure_canvas_agg.get_renderer()._renderer, (0, 1, 2, 3))

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo


root = tk.Tk()
root.wm_title("Put Option Strategy")
w, h = 1000, 700
canvas = tk.Canvas(root, width=w, height=h)
canvas.pack()

# # Generate some example data
X = np.linspace(0, 2 * np.pi, 50)
Y = np.sin(X)

# # create figure for plotting
fig = Figure(figsize=(3, 2), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_ylabel('Premium Collected')
ax.set_title('Pareto Curve for Best Options (Puts)')
ax.plot(X, Y)


# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)



# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()


# Keep this handle alive, or else figure will disappear
fig_x, fig_y = 500, 0
fig_photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))
fig_w, fig_h = fig_photo.width(), fig_photo.height()

# Add more elements to the canvas, potentially on top of the figure
canvas.create_line(200, 50, fig_x + fig_w / 2, fig_y + fig_h / 2)
canvas.create_text(200, 50, text="Zero-crossing", anchor="s")




### to collect key press events:
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)
#
# canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tk.Button(master=root, text="Quit", command=_quit)
button.pack(side=tk.BOTTOM)

tk.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.










# stock = 'AAPL'

# aaplCallChain = options.get_calls(stock)
# currentPrice=stock_info.get_live_price(stock)
# info = stock_info.get_quote_table(stock)

# aaplOptions = options.get_calls(stock).plot(x='Strike',y=['Bid','Ask'], xlim=[.5*currentPrice,1.5*currentPrice],title='Bid/Ask Call Spread for {}'.format(stock))
# aaplOptions.axvline(currentPrice, color='green', ls='--')