# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 10:09:28 2017

@author: rain
"""

from tkinter import *
class MenuDemo:
    
    
    def __init__(self):
        
        
        
        window=Tk()
        window.title("Menu Demo")
        menubar=Menu(window)
        window.config(menu=menubar)#Display the menu bar
        #Create a pull-down menu, and add it to the menu bar
        operationMenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Operation",menu=operationMenu)
        operationMenu.add_command(label="Add",command=self.add)
        operationMenu.add_command(label="Subtract",command=self.subtract)
        operationMenu.add_command(label="Multiply",command=self.multiply)
        operationMenu.add_command(label="Divide",command=self.divide)
        
        #create more pull_down menus
        exitmenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Exit",menu=exitmenu)
        exitmenu.add_command(label="Quit",command=window.quit)
        
        #Add a tool bar frame
        frame0=Frame(window)
        frame0.grid(row=1,column=1,sticky = W)
        #Add button to frame0
        Button(frame0,text="+",
               command=self.add).grid(row=1,column=1,sticky = W)
        Button(frame0,text="-",
               command=self.subtract).grid(row=1,column=2)
        Button(frame0,text="*",
               command=self.multiply).grid(row=1,column=3)
        Button(frame0,text="/",
               command=self.divide).grid(row=1,column=4)
               
        #Add labels and entries to frame1
        frame1=Frame(window)
        frame1.grid(row=2,column=1,pady=10)
        Label(frame1,text="Number 1:").pack(side=LEFT)
        self.v1=StringVar()
        Entry(frame1,width=5,textvariable=self.v1,
              justify=RIGHT).pack(side=LEFT)
        Label(frame1,text="Number 2:").pack(side=LEFT)
        self.v2=StringVar()
        Entry(frame1,width=5,textvariable=self.v2,
              justify=RIGHT).pack(side=LEFT)
        Label(frame1,text="Result:").pack(side=LEFT)
        self.v3=StringVar()
        Entry(frame1,width=5,textvariable=self.v3,
              justify=RIGHT).pack(side=LEFT)
             
        frame2=Frame(window)
        frame2.grid(row=3,column=1,pady=10)
        canvas=Canvas(frame2)
        rabbitimage=PhotoImage(file="image/rabbit.gif")
        canvas.create_image(341,192,image=rabbitimage)
        canvas["width"]=683
        canvas["height"]=384
        canvas.pack()
        window.mainloop()
        
    def add(self):
        self.v3.set(eval(self.v1.get())+eval(self.v2.get()))
    def subtract(self):
        self.v3.set(eval(self.v1.get())-eval(self.v2.get()))
    def multiply(self):
        self.v3.set(eval(self.v1.get())*eval(self.v2.get()))
    def divide(self):
        divisor=eval(self.v2.get())
        if divisor==0:
            self.v3.set("The divisor cannot be zero!!!")
        else:
            self.v3.set(eval(self.v1.get())/divisor)
        
MenuDemo()
        
        