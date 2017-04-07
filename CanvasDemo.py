# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 22:25:08 2017

@author: rain
"""

from tkinter import *
class CanvasDemo:
    def displayRect(self):
        self.canvas.create_rectangle(10,10,190,90,tags="rect")
        
    def displayOval(self):
        self.canvas.create_oval(10,10,190,90,fill=,tags=1)
        
    def displayPolygon(self):
        self.canvas.create_arc(10,10,190,90,start=0,
                              extent=90,width=8,fill="red",tags="arc")
    def displayArc(self):
        self.canvas.create_arc(10,10,190,190,start=0,
                               extent=90,width=8,fill="red",tags="arc")
    def displayLine(self):
        self.canvas.create_line(10,10,190,90,fill="red",tags="polygon")
    def displayString(self):
        self.canvas.create_text(60,40,text="Hi,I am a string",
            font="Times 10 bold underline",tags="string")
    def clearCanvas(self):
        self.canvas.delete("rect","oval","arc","polygon","line","string")
                
    def __init__(self):
        window=Tk()
        window.title("Canvas Demo")
        
        #place canvas in the window
        self.canvas=Canvas(window,width=200,height=100,
                           bg="white")
        self.canvas.pack()
        
        #place buttons in frame
        frame=Frame(window)
        frame.pack()
        btRect=Button(frame,text="Rectangle",
                           command=self.displayRect)
        btOval=Button(frame,text="Oval",
                      command=self.displayOval)
        
        btPolygon=Button(frame,text="Polygon",
                         command=self.displayPolygon)
        btArc=Button(frame,text="Arc",
                     command=self.displayArc)
        btLine=Button(frame,text="Line",
                      command=self.displayLine)
        btString=Button(frame,text="String",
                        command=self.displayString)
        btClear=Button(frame,text="Clear",
                       command=self.clearCanvas)
        bt_list=[btRect,btOval,btPolygon,btArc,btLine,btString,btClear]
        for i in range(len(bt_list)):
            bt_list[i].grid(row=1,column=i)
        
        window.mainloop()
            
CanvasDemo()