# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 11:52:37 2017

@author: rain
"""

from tkinter import *
from TkColorName import COLORS
COUNT_LIMIT=60
import matplotlib
color_name=[]
for name in matplotlib.colors.cnames.items():
    color_name.append(name)
class DisplayMandelbrot:
    statistics=[0 for i in range(10)]
    def __init__(self):
        win=Tk()
        win.title("The Mandelbrot Image")
        self.canvas=Canvas(win,height=800,width=800)
        self.canvas.pack()
        self.paint()
        
        #self.test()
        win.mainloop()
    def count(self,c):
        z=(complex(0,0))
        for i in range(COUNT_LIMIT):
            z=z*z+c #Get z1,z2,...
            if abs(z) > 2: return i #The sequence is unbounded 
        
        return COUNT_LIMIT
    def getColor(self,c):
        '''
        colorlist=["midnightblue","navy","darkblue","mediumblue","royalblue",
                   "dodgerblue","deepskyblue","lightskyblue",
                   "lightsteelblue","lightblue"]
        index=9-int(c/COUNT_LIMIT*9)
        self.statistics[index]+=1
        return colorlist[index]
        '''
        return COLORS[c+30]
    def test(self):
        CX=int(self.canvas["width"])/2
        CY=int(self.canvas["height"])/2
        
        y=0
        x=5
        for i in range(10):      
            x=i*20
            self.canvas.create_rectangle(CX+x,CY+y,CX+x+20,CY+y+20,
                                        fill=self.getColor(i)) 
    def paint(self):
        CX=int(self.canvas["width"])/2+100
        CY=int(self.canvas["height"])/2
        print(CX,CY)
        x=-3.0
        multi=200
        dx=dy=0.01
        while x<5.0:
            y=-2.0
            while y<2.0:
                t=complex(x,y)
                c=self.count(t)
                #f c==COUNT_LIMIT #c is in a Mandelbrot set
                #get hex value RRGGBB that is dependent on c           
                #Fill a tiny rectangle with the specified color
                self.canvas.create_rectangle(CX+x*multi,CY+y*multi,
                                             CX+(x+dx)*multi,CY+(y+dy)*multi,
                                             fill=self.getColor(c))
                y+=dy
            
            x+=dx
        print(self.statistics)
            
DisplayMandelbrot()
                                             