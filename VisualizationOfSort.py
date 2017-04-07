# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:50:42 2017

@author: rain
"""
from tkinter import Tk,Frame,Text,Canvas,Button,Entry
from tkinter import LEFT,INSERT,StringVar,IntVar
import tkinter.messagebox
import random

#data[lo,hi]
class Sort:    
    def initVisualFuncs(self,**func):
        self.func=func
        func_keys={"moveout","movein","pmove",
                   "iswap","changeColor"}
        for i in func:
            assert (i in func_keys)
                 
    def InsertSort(self,data,lo,hi):
        if lo==hi:
            return
        
        for i in range(lo+1,hi+1):
            key=data[i]
            self.func["changeColor"](i,"blue")
            j=i-1
            while j>=0 and data[j]>=key:
                data[j+1]=data[j]
                self.func["iswap"](j+1,j)
                j-=1
            data[j+1]=key
        
    def Merge(self,data,lo,mid,hi):
        #先复制在排序会更简单,这个太复杂了
        #print(lo,mid,hi)
        newlst=[0]*(mid-lo+1)
        i=lo
        j=mid+1
        k=lo
        while k<=mid and i<=mid and j<=hi:
            if i<=mid and data[i]>=data[j]:
                newlst[k-lo]=data[i]
                self.func["moveout"](i,k-lo)
                i+=1
                
            elif j<=hi:
                newlst[k-lo]=data[j]
                self.func["moveout"](j,k-lo)
                j+=1
            k+=1
        while k<=mid:
            if i<=mid:
                newlst[k-lo]=data[i]
                self.func["moveout"](i,k-lo)
                i+=1
            if j<=hi:
                newlst[k-lo]=data[j]
                self.func["moveout"](j,k-lo)
                j+=1
            k+=1
        #-------------------------------------
        while k<=hi and i<=mid and j<=hi:
            if i<=mid and data[i]>=data[j]:
                data[k]=data[i]
                self.func["pmove"](i,k)
                i+=1
            elif j<=hi:
                data[k]=data[j]
                self.func["pmove"](j,k)
                j+=1
            k+=1
        while k<=hi:
            if i<=mid:
                self.func["pmove"](i,k)
                data[k]=data[i]
                i+=1
            if j<=hi:
                data[k]=data[j]
                self.func["pmove"](j,k)
                j+=1
            k+=1
        #---------------------------------
        for i in range(lo,mid+1):
            data[i]=newlst[i-lo]
            self.func["movein"](i-lo,i)
        #print(lo,mid,hi)
        #print(data[lo:hi+1])
        
    def MergSort(self,data,lo,hi):
        if lo<hi:
            mid=(lo+hi)//2
            
            self.MergSort(data,lo,mid)
            self.MergSort(data,mid+1,hi)
            self.Merge(data,lo,mid,hi)
            #print(data)
    
    def parition(self,data,lo,hi):
        pivot=data[lo]
        self.func["changeColor"](lo,"blue")
        i=lo
        j=hi
        
        while True:
            while(data[i]<pivot and i!=j):
                i+=1
            while(data[j]>pivot and i!=j):
                j-=1        
            if i>=j:
                return j
            data[i]+=data[j]
            data[j]=data[i]-data[j]
            data[i]=data[i]-data[j]
            self.func["iswap"](i,j)


    def QuickSort(self,data,lo,hi):
        if lo<hi:
            p=self.parition(data,lo,hi)
            self.QuickSort(data,lo,p-1)
            self.QuickSort(data,p+1,hi)
 
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
    
    def __init__(self):
      
        window=Tk()
        window.title("Canvas Demo")
        
        rightFrame=Frame(window)
        rightFrame.grid(row=1,column=2)
        self.text=Text(rightFrame,width=60)
        self.text.grid()   
        
        leftFrame=Frame(window)
        leftFrame.grid(row=1,column=1)
        sframe=Frame(leftFrame)
        sframe.pack()
        self.canvas=Canvas(sframe,bg="White",
                           width=self.win_width,height=self.win_height)
        self.canvas.pack()
        

        bframe=Frame(leftFrame)
        bframe.pack()
        self.count=20
        self.tbcount=IntVar()
        self.tbcount.set(self.count)
        Entry(bframe,textvariable=self.tbcount,width=5).pack(side=LEFT)
        Button(bframe,text="Initialization",
               command=self.processInit).pack(side=LEFT)
        Button(bframe,text="InsertSort",
               command=self.processInsertSort).pack(side=LEFT)
        Button(bframe,text="MergeSort",
               command=self.processMergeSort).pack(side=LEFT)
        Button(bframe,text="QuickSort",
               command=self.processFastSort).pack(side=LEFT)
        self.tbspeed=IntVar()
        self.speed=200
        self.tbspeed.set(self.speed)
        Entry(bframe,textvariable=self.tbspeed,width=5).pack(side=LEFT)
        Button(bframe,text="ChangeSpeed",
               command=self.changeSpeed).pack(side=LEFT)
        mysort=Sort() 
        mysort.initVisualFuncs(
                moveout=self.moveout,
                movein=self.movein,
                pmove=self.pmove,
                iswap=self.iswap,
                changeColor=self.changeColor
                )
        self.sortEngine=mysort
        
        self.initData()
        
        window.mainloop()
    def changeSpeed(self):
        self.speed=self.tbspeed.get()
        self.iprint("the speed of move change to "+str(self.speed)+"\n")
    def initData(self):
        self.count=self.tbcount.get()
        self.data=[i for i in range(self.count)]
        data=self.data
        random.shuffle(data)
        self.old_data=data[::]
                
        #initialization of data
        length=len(data)
        self.per_width=self.win_width/length
        self.proportion=self.win_height/max(data)*0.9/2
        self.iprint(data)
        
        
        #visualization of data
        for i in range(length):
           self.drawRect(i,data[i]) 
        
        self.rect_pos=[]
        for i in self.canvas.find_withtag("all"):
            self.rect_pos.append(i)
        #self.iprint(self.rect_pos)
        self.rect_pos2=self.rect_pos[::]  
        
           
    def processInit(self):
        self.canvas.delete("all")
        self.initData()                        
        self.canvas.update() 
        
    def drawRect(self,ordinal,data_y):
        h=data_y*self.proportion
        self.uprow_h=self.win_height-2*h
        LB_x=ordinal*self.per_width
        self.canvas.create_rectangle(
            LB_x,self.win_height-h,
            LB_x+self.per_width,self.win_height,
            outline="red",
            tags=ordinal)
    def iswap(self,ord1,ord2):
        diff_ord=ord2-ord1
        flag=1 if diff_ord>0 else -1
        for i in range(abs(diff_ord)):
            self.canvas.move(self.rect_pos[ord1],flag*self.per_width,0)
            self.canvas.move(self.rect_pos[ord2],-flag*self.per_width,0)
            self.canvas.update()
            self.canvas.after(self.speed)
        self.rect_pos[ord1]+=self.rect_pos[ord2]
        self.rect_pos[ord2]=self.rect_pos[ord1]-self.rect_pos[ord2]
        self.rect_pos[ord1]=self.rect_pos[ord1]-self.rect_pos[ord2]
        #print(self.rect_pos)
     
    def changeColor(self,ord1,color):
        self.canvas.itemconfig(self.rect_pos[ord1],outline=color)
    
    def pmove(self,ord1,ord2):
        diff_ord=ord2-ord1
        flag=1 if diff_ord>0 else -1
        for i in range(abs(diff_ord)):
            self.canvas.move(self.rect_pos[ord1],flag*self.per_width,0)
            self.canvas.update()
            self.canvas.after(self.speed)
        self.rect_pos[ord2]=self.rect_pos[ord1]
    def moveout(self,ord_in,ord_out):
        diff_ord=ord_out-ord_in
        flag=1 if diff_ord>0 else -1
        self.canvas.move(self.rect_pos[ord_in],0,-250)
        self.canvas.after(self.speed)
        self.canvas.update()
        for i in range(abs(diff_ord)):
            self.canvas.move(self.rect_pos[ord_in],flag*self.per_width,0)
            self.canvas.update()
            self.canvas.after(self.speed)
        
        self.rect_pos2[ord_out]=self.rect_pos[ord_in]
        
    def movein(self,ord_out,ord_in):
        diff_ord=ord_out-ord_in
        flag=-1 if diff_ord>0 else 1
        for i in range(abs(diff_ord)):
            self.canvas.move(self.rect_pos2[ord_out],flag*self.per_width,0)
            self.canvas.update()
            self.canvas.after(self.speed)
        self.canvas.move(self.rect_pos2[ord_out],0,250)
        self.canvas.update()
        self.rect_pos[ord_in]=self.rect_pos2[ord_out]
        self.canvas.after(self.speed)
        
   
    def processFastSort(self):
        #tkinter.messagebox.showerror("sorry","The function is building")
        data=self.data
        self.sortEngine.QuickSort(data,0,len(data)-1)
        self.iprint(data)
        
    def processInsertSort(self):
        data=self.data
        self.sortEngine.InsertSort(data,0,len(data)-1)
        self.iprint(data)
    def processMergeSort(self):
        data=self.data
        self.sortEngine.MergSort(data,0,len(data)-1)
        self.iprint(data)

    def iprint(self,content):
        if type(content)==str:
            istr=content+'\n'
        elif type(content)==list:
            istr="\nList: "
            istr=istr+''.join(["%d,"%(i) for i in content])
        self.text.insert(INSERT,istr)

if __name__=="__main__":    
 
    myvisual=Visualization()
    
    