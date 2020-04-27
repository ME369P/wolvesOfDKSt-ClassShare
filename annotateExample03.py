# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 17:33:10 2020

@author: ZiamG
"""


from matplotlib import pyplot as plt
import mplcursors
from pandas import DataFrame


df = DataFrame(
    [("Alice", 163, 54),
     ("Bob", 174, 67),
     ("Charlie", 177, 73),
     ("Diane", 168, 57)],
    columns=["name", "height", "weight"])

df.plot.scatter("height", "weight")
mplcursors.cursor(hover = True).connect(
    "add", lambda sel: sel.annotation.set_text(df["name"][sel.target.index]))
plt.show()

# test: skip