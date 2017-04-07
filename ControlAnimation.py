# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:55:11 2017

@author: rain
"""

from tkinter import *

class ControlAnimation:
    def __init__(self):
        window=Tk()
        window.title("Control Animation Demo")
        
        self.width=250
        self.canvas=Canvas(window,bg="white",
                           width=self.width,height=50)
        self.canvas.pack()
        
        self.x=0
        self.dx=3
        self.sleepTime=100
        self.canvas.create_text(self.x,30,
            text="Message moving",tags=1)
        self.isStopped=False
        
        frame=Frame(window)
        frame.pack()
        Button(frame,text="Stop",
               command=self.stop).pack(side=LEFT)
        Button(frame,text="Resume",
               command=self.resume).pack(side=LEFT)
        Button(frame,text="Faster",
               command=self.faster).pack(side=LEFT)
        Button(frame,text="Slower",
               command=self.slower).pack(side=LEFT)    
               
        self.animate()
        window.mainloop()
        
    def stop(self):
        self.isStopped=True
    def resume(self):
        self.isStopped=False
        self.animate()
        
    def animate(self):
        while not self.isStopped:
            self.canvas.move(1,self.dx,0)#Move text
            self.canvas.after(self.sleepTime)
            self.canvas.update()#Update canvas
            self.x+=self.dx
            if self.x>self.width:
                self.x=0
                self.canvas.delete("text")
                self.canvas.create_text(self.x,30,
                                        text="Message moving",tags=1)
            #print(self.x,end=' ')
    def faster(self):
        self.sleepTime-=20
    def slower(self):
        self.sleepTime+=20
        
ControlAnimation()