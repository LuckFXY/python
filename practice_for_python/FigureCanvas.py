# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 11:17:34 2017

@author: rain
"""

from tkinter import *

class FigureCanvas(Canvas):
        
    def __init__(self,container,figureType,width=100,height=100):
        super().__init__(container,width=width,height=height)
    def drawFigure(self):
        func_list=[displayRect,displayOval,displayPolygon,displayArc]
        func_list[self.__figure]()
    def displayRect(self):
        w=int(self["width"])
        h=int(self["height"])
        self.canvas.create_rectangle(10,10,w-10,h-10,tags="rect")
        
    def displayOval(self):
        w=int(self["width"])
        h=int(self["height"])
        self.canvas.create_oval(10,10,w-10,h-10,fill="red",tags=1)
        
    def displayPolygon(self):
        w=int(self["width"])
        h=int(self["height"])
        self.canvas.create_arc(10,10,w-10,h-10,start=0,
                              extent=90,width=8,fill="red",tags="arc")
    def displayArc(self):
        w=int(self["width"])
        h=int(self["height"])
        self.canvas.create_arc(10,10,190,190,start=0,
                               extent=90,width=8,fill="red",tags="arc")
    
    def clearCanvas(self):
        
        self.canvas.delete("rect","oval","arc","polygon","line","string")