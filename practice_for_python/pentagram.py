# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 15:53:29 2017

@author: rain
"""

import turtle as tu
import math
def star():
    tu.penup()
    tu.goto(-100,100)
    tu.pendown()

    for i in range(5):
        tu.forward(200)
        tu.right(144)
    

def triangle(p1,p2):
    x1,y1=p1
    x2,y2=p2
    tu.penup()
    #bottom left point
    length=math.sqrt((x2-x1)**2+(y2-y1)**2)
    #print(p1,p2)
    tu.goto(x1,y1)
    tu.pendown()
    
    angle=math.atan((y2-y1)/(x2-x1))/math.pi*180
    if(x2<x1):
        angle+=180
    print(angle)
    tu.setheading(angle)
    for i in range(3):
        tu.forward(length)
        tu.left(120)
     
plist=[]

def hexagon(start_x,start_y,pointlist):
    tu.penup()
    tu.goto(start_x,start_y)
    tu.pendown()
    tu.right(60)
    for i in range(6):
        tu.forward(100)
        tu.left(60)
        pointlist.append((tu.xcor(),tu.ycor()))
        #print(pointlist[-1])
hexagon(-100,0,plist)


for i in range(6):
    triangle(plist[i],plist[(i+2)%6])
    
for i in range(6):
    tu.penup()
    tu.goto(plist[i])
    tu.pendown()
    tu.goto(plist[(i+3)%6])
tu.done()
