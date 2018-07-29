# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 21:56:30 2017

@author: rain
"""

from tkinter import Tk,Canvas,Frame,Label,Entry,Button
from tkinter import LEFT,StringVar,RIGHT
from math import sin,cos,sqrt
class SierpinskiTriangle:
    def __init__(self):
        win=Tk()
        win.title("Sierpinski Triangle")
        self.width=400
        self.height=400
        leftframe=Frame(win)
        leftframe.grid(row=1,column=1)
        self.canvas=Canvas(leftframe,
            width=self.width,height=self.height)
        
        self.canvas.pack()
        
        #Add a label,an entry, and a button to frame1
        frame1=Frame(leftframe)
        frame1.pack()
        
        Label(frame1,
              text="Enter an order").pack(side=LEFT)
        self.order=StringVar()
        Entry(frame1,textvariable=self.order,
                    justify=RIGHT).pack(side=LEFT)
        Button(frame1,text="Display Sierpinski Triangle",
               command=self.display).pack(side=LEFT)
        self.order.set(0)
        rightframe=Frame(win)
        rightframe.grid(row=1,column=2)
        
        self.canvas2=Canvas(rightframe,
            width=self.width,height=self.height)
        self.canvas2.pack()
        frame2=Frame(rightframe)
        frame2.pack()
        Label(frame2,
              text="Enter an order").pack(side=LEFT)
        self.order2=StringVar()
        Entry(frame2,textvariable=self.order2,
                    justify=RIGHT).pack(side=LEFT)
        self.order2.set(0)
        Button(frame2,text="Display Snowflake",
               command=self.display2).pack(side=LEFT)
        self.display()
        self.display2()
        win.mainloop()
    def display(self):
        self.canvas.delete("line")
        p1=[self.width/2,10]
        p2=[10,self.height-10]
        p3=[self.width-10,self.height-10]
        self.displayTriangles(int(self.order.get()),p1,p2,p3)
    def display2(self):
        self.canvas2.delete("line2")
        padding=self.width/4
        p1=[self.width/2,padding]
        p2=[padding,self.height-padding]
        p3=[self.width-padding,self.height-padding]
        self.displaySnowflake(int(self.order2.get()),p1,p2,p3)    
    def midpoint(self,p1,p2):
        p=2*[0]
        p[0]=(p1[0]+p2[0])/2
        p[1]=(p1[1]+p2[1])/2
        return p
    def drawLine(self,p1,p2):
        self.canvas.create_line(p1[0],p1[1],p2[0],p2[1],
                                tags="line")
    def drawLine2(self,p1,p2):
        self.canvas2.create_line(p1[0],p1[1],p2[0],p2[1],
                                tags="line2")
    def displayTriangles(self,order,p1,p2,p3):
        if order==0:
            self.drawLine(p1,p2)
            self.drawLine(p2,p3)
            self.drawLine(p3,p1)
        else:
            p12=self.midpoint(p1,p2)
            p23=self.midpoint(p2,p3)
            p13=self.midpoint(p3,p1)
            
            #Recursiely display three triangles
            self.displayTriangles(order-1,p1,p12,p13)
            self.displayTriangles(order-1,p12,p2,p23)
            self.displayTriangles(order-1,p23,p13,p3)
    def distance(self,p1,p2):
        return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
    def displaySnowflake(self,order,p1,p2,p3):
        if order==0:
            self.drawLine2(p1,p2)
            self.drawLine2(p2,p3)
            self.drawLine2(p3,p1)
        else:         
            #Recursiely display three triangles
            
            self.displaySnowflake_inside(order-1,p2,p1)
            self.displaySnowflake_inside(order-1,p1,p3)
            self.displaySnowflake_inside(order-1,p3,p2)
    def getPM(self,p1,p2):
        pm=self.midpoint(p1,p2)
        length=self.distance(p1,p2)*sqrt(3)/2
        dx=p2[0]-p1[0]
        dy=p2[1]-p1[1]
        tiny=1
        if abs(dy)<tiny:
            if dx>0:
                pm[1]-=length
            else: 
                pm[1]+=length
            
        else:
            if dy<0:
                pm[0]-=length*sqrt(3)/2
            else:
                pm[0]+=length*sqrt(3)/2 
            if dx>0:
                pm[1]-=length/2        
            else:
                pm[1]+=length/2                
        return pm
    
    def displaySnowflake_inside(self,order,p1,p2): 
        p11=[(2*p1[0]+p2[0])/3,
             (2*p1[1]+p2[1])/3]
        p12=[(p1[0]+2*p2[0])/3,
             (p1[1]+2*p2[1])/3]
        pm=self.getPM(p11,p12)
        if order==0:                                       
            self.drawLine2(p1,p11)
            self.drawLine2(p11,pm)
            self.drawLine2(pm,p12)
            self.drawLine2(p12,p2)
        else:
            self.displaySnowflake_inside(order-1,p1,p11)
            self.displaySnowflake_inside(order-1,p11,pm)
            self.displaySnowflake_inside(order-1,pm,p12)
            self.displaySnowflake_inside(order-1,p12,p2)
            
            
SierpinskiTriangle()
            