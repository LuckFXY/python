# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 09:32:08 2017

@author: rain
"""
from tkinter import *
class PackMangerDemo:
    def ProcessButton(self):
        ch=self.testVar.get()
        ch+="烫"
        self.testVar.set(ch)
        num=self.testVar2.get()
        self.testVar2.set(int(num)+5)
    def __init__(self):
        window=Tk()
        window.title("pack Manager Demo")
        
        frame1=Frame(window)
        frame1.grid(row=1,column=1)
        Label(frame1,text="Blue",bg="blue").pack()
        Label(frame1,text="Red",bg="red").pack(
        fill=BOTH,expand=1)
        Label(frame1,text="Green",bg="green").pack(
        fill=BOTH)
        
    #--------------------------------
        frame2=Frame(window)
        frame2.grid(row=2,column=1)
        Label(frame2,text="Blue",bg="blue").pack(side=LEFT)
        Label(frame2,text="Red",bg="red").pack(
        fill=BOTH,expand=1,side=LEFT)
        Label(frame2,text="Green",bg="green").pack(
        fill=BOTH,side=LEFT)
    #-----------------------------------     
        frame3=Frame(window)
        #frame3.place(x=100,y=100)
        frame3.grid(row=3,column=1)
        Label(frame3,text="Label",bg="purple").pack(side=LEFT)
        self.testVar=StringVar()
        self.testVar2=StringVar()
        self.testVar.set(1)
        self.testVar2.set(1)
        Entry(frame3,textvariable=self.testVar).pack(side=LEFT)
        Entry(frame3,textvariable=self.testVar2).pack(side=LEFT)
        Button(frame3,text="Point me",
               command=self.ProcessButton).pack(side=LEFT)
        
        window.mainloop()
        
        #Label.place(x=,y=)
PackMangerDemo()
        
        