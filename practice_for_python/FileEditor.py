# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 20:05:43 2017

@author: rain
"""

from tkinter import*
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
#create a menu bar
class FileEditor:
    def __init__(self):
        win=Tk()
        win.title("Simple Text Editor")
        
        #Create a menu bar
        menubar=Menu(win)
        win.config(menu=menubar)
        
        #Create a pull-down  menu 
        operationMenu=Menu(menubar,tearoff=0)
        #add it to the menu bar
        menubar.add_cascade(label="File",menu=operationMenu)
        #crate submenu and add it to the menu of File
        operationMenu.add_command(label="Open",
                          command=self.openFile)
        operationMenu.add_command(label="Save",
                          command=self.saveFile)
                          
        #add a tool bar frame
        frame0=Frame(win)
        frame0.grid(row=1,column=1,sticky=W)
        
        #create image
        openImg=PhotoImage(file="image/open.gif")
        saveImg=PhotoImage(file="image/save.gif")
        
        Button(frame0,image=openImg,command=self.openFile,
               ).grid(row=1,column=1,sticky=W)
        Button(frame0,image=saveImg,command=self.saveFile,
               ).grid(row=1,column=2)
               
        frame1=Frame(win)
        frame1.grid(row=2,column=1)
        #create a scrollbar
        scrollbar=Scrollbar(frame1)
        #set a layout for scrollbar
        scrollbar.pack(side=RIGHT,fill=Y)
        #add the scrollbar to the window
        self.text=Text(frame1,width=40,height=20,
                       wrap=WORD,yscrollcommand=scrollbar.set)
                       
        self.text.pack()
        #set the config of scrollbar
        scrollbar.config(command=self.text.yview)
        win.mainloop()
                          
    def openFile(self):
        filenameforReading=askopenfilename()
        infile=open(filenameforReading,"r")
        self.text.insert(END,infile.read())
        infile.close()
        
    def saveFile(self):
        filenameforWriting=asksaveasfilename()
        outfile=open(filenameforWriting,"w")
        outfile.write(self.text.get(1.0,END))
        outfile.close()

FileEditor()