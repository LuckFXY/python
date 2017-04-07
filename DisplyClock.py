# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 10:25:04 2017

@author: rain
"""

from tkinter import *
from StillClock import StillClock
class DisplayClock:
    def __init__(self):
        self.window=Tk()
        self.window.title("Change Clock Time")
        
        self.clock=StillClock(self.window)
        self.clock.pack()
        
        self.frame=Frame(self.window)
        self.frame.pack()
        frame=self.frame
        Label(frame,text="Hour:").pack(side=LEFT)
        self.hour=IntVar()
        self.hour.set(self.clock.getHour())
        Entry(frame,textvariable=self.hour,width=2).pack(side=LEFT)
        
        Label(frame,text="Minute:").pack(side=LEFT)
        self.minute=IntVar()
        self.minute.set(self.clock.getMinute())
        Entry(frame,textvariable=self.minute,width=2).pack(side=LEFT)
        
        Label(frame,text="Second:").pack(side=LEFT)
        self.second=IntVar()
        self.second.set(self.clock.getSecond())
        Entry(frame,textvariable=self.second,width=2).pack(side=LEFT)
        
        Button(frame,text="Set New Time",
               command=self.setNewTime).pack(side=LEFT)
        Button(frame, text="QUIT", fg="red",
               command=self.closeWindow).pack(side=LEFT)
        self.clock.walk()
        
        self.window.mainloop()
        
    def setNewTime(self):
        self.clock.setTime(
            self.hour.get(),self.minute.get(),self.second.get()
        )
    def closeWindow(self):
        self.clock.stopwalk()
        self.window.destroy()
        
DisplayClock()