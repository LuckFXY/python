# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 22:35:37 2017

@author: rain
"""

from tkinter import *
'''
def processOK():
    print("OK button is clicked")
    
def processCancel():
    print("Cancel button is clicked")
window=Tk()
label=Label(window,text="Welcome to Python")
btOK=Button(window,text="OK",fg="red",command=processOK)
btCancel=Button(window,text="Cancel",bg="yellow",command=processCancel)
label.pack()
btOK.pack()
btCancel.pack()
window.mainloop()'''

class WidgetDemo:
    def processCheckbutton(self):
        self.text.insert(END,"check button is "+
        ("check" if self.v1.get()==1 else "unckecked")+'\n')
    def processRadiobuttion(self):
       self.text.insert(END,"the color was selected is "+
        ("red" if self.v2.get()==1 else "yellow")+'\n')
    def processButton(self):
        self.text.insert(END,"Your name is "+self.name.get()+'\n')
        
    def __init__(self):
        window=Tk()
        window.title("Widgets Demo")
        
        frame1=Frame(window)
        frame1.pack()
        '''
        Tkinter中一些组件(Button, Label等) 
        如果设置一个textvariable属性为一个StringVar(IntVar, DoubleVar)对象。
        当这个对象的值被重新设置的时候，组件上的显示文字就会自动变成新的值。
        '''
        self.v1=IntVar()
        
        cbtBold=Checkbutton(frame1,text="Bold",
            variable=self.v1,command=self.processCheckbutton)
        
        self.v2=IntVar()
        rbtRed=Radiobutton(frame1,text="Red",bg="Red",
            variable=self.v2,value=1,
            command=self.processRadiobuttion)
        rbtYellow=Radiobutton(frame1,text="Yellow",bg="Yellow",
            variable=self.v2,value=2,
            command=self.processRadiobuttion)
        cbtBold.grid(row=1,column=1)
        rbtRed.grid(row=1,column=2)
        rbtYellow.grid(row=1,column=3)
        
        frame2=Frame(window)
        frame2.pack()
        label=Label(frame2,text="Enter your name: ")
        self.name=StringVar()
        entryName=Entry(frame2,textvariable=self.name)
        btGetName=Button(frame2,text="Get Name",
                         command=self.processButton)
        message=Message(frame2,text="It is a widgets demo")
        label.grid(row=1,column=1)
        entryName.grid(row=1,column=2)
        btGetName.grid(row=1,column=3)
        message.grid(row=1,column=4)
        
        self.text=Text(window)
        self.text.pack()
        window.mainloop()
        
WidgetDemo()

        
        