# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:11:23 2017

@author: rain
"""
#for free

from tkinter import Tk,Frame,Canvas,PhotoImage,Radiobutton,Entry,Button,Label
from tkinter import  IntVar,BooleanVar
from tkinter import  LEFT
from PIL import Image,ImageTk
import os
from collections import Iterable
import tkinter.messagebox
import sqlite3
class MyIO:
    
    def __init__(self,foldername):
        self.index=0
        self.filelist=[]
        self.len_filelist=0
        if os.path.exists(foldername)==False:
            tkinter.messagebox.showerror("error",("folder: %s does exist")%(foldername))
        scan_folder(foldername)
        
        
    def scan_folder(self,file_dir):
        for root,dirs,files in os.walk(file_dir):
            for file in files:
                postfix=os.path.splitext(file)[1]
                if postfix in {'bmp','png','jpg'}:
                    filename=os.path.join(root,file)
                    self.filelist.append(filename)
    def getIndex():
        return self.index
    def setIndex(num):
        self.index=num
    def myiter(self):
        while self.index < self.len_filelist:
            yield(self.filelist[i])
            self.index=+1      
        return 'done'
    '''
    while true:
        try:
            x=next(g)
        except StopInteration as e:
            print("generator return value",e.value)
            break
    '''
    def createdb():
        if os.path.exists('result.db')==False:
            conn=sqlite3.connect('example.db')
            c= conn.cursor()
            
            c.execute('''
                  CREATE TABLE data
                  (filename text,
                  InCir_R int,InCir_X int, InCir_Y int,
                  OutCir_R int,OutCir_X int, OutCir_Y int)
                  ''')
            c.execute("INSERT INTO data VALUES ('1.bmp',1,2,3,4,5,6)")
            conn.commit()
            conn.close()
    def savetodb(block):
        #filename,InCir_R,InCir_X, InCir_Y,OutCir_R,OutCir_X, OutCir_Y=block
        conn=sqlite3.connect('example.db')
        c= conn.cursor()
        c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?)",block)
        conn.commit()
        conn.close()
    def update(filename,block):
        conn=sqlite3.connect('example.db')
        c= conn.cursor()
        block.append(filename)
        c.execute("update data set\
                  (filename,InCir_R,InCir_X, InCir_Y,OutCir_R,OutCir_X, OutCir_Y)\
                  = (?,?,?,?,?,?,?) where filename = ?",block)
        conn.commit()
        conn.close()
        
class MainWindow:
    
    image_index=0
    ImageCount=0
    canvas=None
    Image_list=[]
    x1,x2,y1,y2=(0,0,0,0)
    def processLButton(self):
        print()
        
    def processRButton(self):
        print()
        
    def processChooseInner(self):
        self.isInnerCircle=True
    def processChooseOutside(self):
        self.isInnerCircle=False
        
    def processOk(self):
        print()
    #--------------draw a circle
    def Press(self,event):
        self.x1=event.x
        self.y1=event.y
    
    def _DrawCircle(self,moving=True,update=False):
        ch='inner'
        if self.isInnerCircle== False:
            ch='outside'
        if update:
            self.canvas.delete(ch)
        d=self.x2-self.x1
        if not self.canvas.find_withtag(ch):
            self.canvas.create_oval(
                self.x1,self.y1,self.x1+d,self.y1+d,
                outline='red',tags=ch)
        elif moving:
            self.canvas.delete(ch)
            
        if self.isInnerCircle:
            self.inner_r.set(d//2)
            self.inner_x.set(self.x1+d/2)
            self.inner_y.set(self.y1+d/2)
        else:
            self.outside_r.set(d//2)
            self.outside_x.set(self.x1+d//2)
            self.outside_y.set(self.y1+d//2)

        
    def Draw(self,event):
        self.x2=event.x
        self.y2=event.y
        self._DrawCircle()
    def PressKey(self,event):
       key=event.keysym

       if key=='w':
           self.y1-=1
           self.y2-=1
       elif key=='s' :
           self.y1+=1
           self.y2+=1
       elif key=='a' :
           self.x1-=1
           self.x2-=1
       elif key== 'd':
           self.x1+=1
           self.x2+=1
           
       elif key =='q':
           self.x2-=1
           self.y2-=1
       elif key =='e':
           self.x2+=1
           self.y2+=1
       self._DrawCircle(moving=False,update=True)
           
           
           
    def __init__(self):
        
        window=Tk()
        window.title("Assist Tool")
        default_image=Image.open("iris_sample/002L_2.png")
        default_image=ImageTk.PhotoImage(default_image)
        
        leftimage=PhotoImage(file="image/left.gif")
        rightimage=PhotoImage(file="image/right.gif")
        okimage=PhotoImage(file="image/ok.gif")
        self.inner_x=IntVar()
        self.inner_y=IntVar()
        self.inner_r=IntVar()
        self.outside_x=IntVar()
        self.outside_y=IntVar()
        self.outside_r=IntVar()
        self.h=default_image.height()
        self.w=default_image.width()
        self.filename='filename'
        self.isInnerCircle=BooleanVar()
        self.isInnerCircle.set(True)
        
        frame_left=Frame(window)
        frame_left.grid(row=1,column=1)
        frame_right=Frame(window)
        frame_right.grid(row=1,column=2)
        frame_right_1=Frame(frame_right)
        frame_right_1.grid(row=1,column=1)
        frame_right_2=Frame(frame_right)
        frame_right_2.grid(row=2,column=1)
        frame_right_3=Frame(frame_right)
        frame_right_3.grid(row=3,column=1)
        frame_right_4=Frame(frame_right)
        frame_right_4.grid(row=4,column=1)
        frame_right_5=Frame(frame_right)
        frame_right_5.grid(row=5,column=1)
        
        #---------------show picture------
        self.canvas=Canvas(frame_left)
        
        self.canvas["width"]=self.w+100
        self.canvas["height"]=self.h+100
        self.canvas.create_image(self.w//2,self.h//2,image=default_image)
        self.canvas.pack()
        self.canvas.bind('<Button-1>',self.Press)
        self.canvas.bind('<B1-Motion>',self.Draw)
        window.bind('<Key>',self.PressKey)
        #--------------show filename 
        self.label_filename=Label(frame_right_1,text=self.filename)
        self.label_filename.pack()  
        #-------------control button
        Button(frame_right_2,image=leftimage,
               command=self.processLButton).pack(side=LEFT)
        Button(frame_right_2,image=rightimage,
               command=self.processRButton).pack(side=LEFT)
        #-------------show info of inner circle
        self.radio_innerCircle=Radiobutton(frame_right_3,text="Inner Circle",
            command=self.processChooseInner,variable=self.isInnerCircle,value=True)
        self.radio_innerCircle.grid(row=1,column=2)
        Label(frame_right_3,text="r").grid(row=2,column=1)
        self.entry_inner_r=Entry(frame_right_3,textvariable=self.inner_r)
        self.entry_inner_r.grid(row=2,column=2)
        Label(frame_right_3,text="x").grid(row=3,column=1)
        self.entry_inner_x=Entry(frame_right_3,textvariable=self.inner_x)
        self.entry_inner_x.grid(row=3,column=2)
        Label(frame_right_3,text="y").grid(row=4,column=1)
        self.entry_inner_y=Entry(frame_right_3,textvariable=self.inner_y)
        self.entry_inner_y.grid(row=4,column=2)
        #------------show info of outside circle
        self.radio_outsideCircle=Radiobutton(frame_right_4,text="Outside Circle",
            command=self.processChooseOutside,variable=self.isInnerCircle,value=False)
        self.radio_outsideCircle.grid(row=1,column=2)        
        Label(frame_right_4,text="r").grid(row=2,column=1)
        self.entry_outside_r=Entry(frame_right_4,textvariable=self.outside_r)
        self.entry_outside_r.grid(row=2,column=2)
        Label(frame_right_4,text="x").grid(row=3,column=1)
        self.entry_outside_x=Entry(frame_right_4,textvariable=self.outside_x)
        self.entry_outside_x.grid(row=3,column=2)
        Label(frame_right_4,text="y").grid(row=4,column=1)
        self.entry_outside_y=Entry(frame_right_4,textvariable=self.outside_y)
        self.entry_outside_y.grid(row=4,column=2)        
        #-------------ok button
        Button(frame_right_5,image=okimage,
               command=self.processOk).pack(side=LEFT)
        #-------------finally---------     
        self.radio_innerCircle.select()
        window.mainloop()
        
MainWindow()