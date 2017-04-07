# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 09:56:14 2017

@author: rain
"""

from tkinter import *
import tkinter.messagebox
import random

def ishuffle(lst):
    length=len(lst)-1
    for i in range(length):
        r=random.randint(i,length)
        temp=lst[i]
        lst[i]=lst[r]
        lst[r]=temp
        
class Visualization:
    win_width=500
    win_height=500
    per_width=1
    rect_pos=[]
    def __init__(self,data):
        #the type of data is np.arry
        assert type(data)==list
        self.data=data
        
        window=Tk()
        window.title("Canvas Demo")
        
        rightFrame=Frame(window)
        rightFrame.grid(row=1,column=2)
        self.text=Text(rightFrame)
        self.text.grid()   
        
        leftFrame=Frame(window)
        leftFrame.grid(row=1,column=1)
        sframe=Frame(leftFrame)
        sframe.pack()
        self.canvas=Canvas(sframe,bg="White",
                           width=self.win_width,height=self.win_height)
        self.canvas.pack()
        length=len(data)
        self.per_width=self.win_width/length
        self.proportion=self.win_height/max(data)*0.9
        
        self.rect_pos=[i for i in range(1,length+1)]
            
        self.iprint(self.rect_pos)        
        self.iprint(data)
        
        for i in range(length):
           self.drawRect(i,data[i]) 

        bframe=Frame(leftFrame)
        bframe.pack()
        Button(bframe,text="Initialization",
               command=self.processInit).pack(side=LEFT)
        Button(bframe,text="InsertSort",
               command=self.processInsertSort).pack(side=LEFT)
        Button(bframe,text="FastSort",
               command=self.processFast).pack(side=LEFT)
               
        
        window.mainloop()
        
        
    def drawRect(self,ordinal,data_y):
        h=data_y*self.proportion
        LB_x=ordinal*self.per_width
        self.canvas.create_rectangle(
            LB_x,self.win_height-h,
            LB_x+self.per_width,self.win_height,
            outline="red",
            tags=self.rect_pos[ordinal])
    def iswap(self,ord1,ord2):
        diff_ord=ord2-ord1
        flag=1 if diff_ord>0 else -1
        for i in range(abs(diff_ord)):
            self.canvas.move(self.rect_pos[ord1],flag*self.per_width,0)
            self.canvas.move(self.rect_pos[ord2],-flag*self.per_width,0)
            self.canvas.update()
            self.canvas.after(100)
        self.rect_pos[ord1]+=self.rect_pos[ord2]
        self.rect_pos[ord2]=self.rect_pos[ord1]-self.rect_pos[ord2]
        self.rect_pos[ord1]=self.rect_pos[ord1]-self.rect_pos[ord2]
        #print(self.rect_pos)
    def processInit(self):
        data=self.data
        ishuffle(data)
        
        self.canvas.delete("all")
        self.canvas.update()
        self.canvas.after(500)
        for i in range(len(data)):
           self.drawRect(i,data[i])
        self.rect_pos=[]
        for i in self.canvas.find_withtag("all"):
            self.rect_pos.append(i)
        self.canvas.update()   
           
    def processInsertSort(self):
        data=self.data
        length=len(data)
        for i in range(1,length):
            key=data[i]
            j=i-1
            while j>=0 and data[j]>=key:
                data[j+1]=data[j]
                self.iswap(j+1,j)
                j-=1
            data[j+1]=key
            self.iprint(data)
    def processFast(self):
        tkinter.messagebox.showerror("sorry","The function is building")
    def iprint(self,content):
        if type(content)==str:
            istr+='\n'
        elif type(content)==list:
            istr="\nList: "
            istr=istr+''.join(["%d,"%(i) for i in content])
        self.text.insert(INSERT,istr)


if __name__=="__main__":
    data=[i for i in range(20)]
    ishuffle(data)
    
    Visualization(data)