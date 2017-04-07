# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 11:24:01 2017

@author: rain
"""

from tkinter import *
from FigureCanvas import FigureCanvas

class DisplayFigures:
    def __init__(self):
        win=Tk()
        win.title("Display Figure")
        for i in range(4):
            FigureCanvas(win,i).pack(side=LEFT)
        win.mainloop()
        
DisplayFigures()
        