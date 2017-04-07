# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:12:26 2017

@author: rain
"""
import turtle
from random import randint
turtle.speed(0)
turtle.color("gray")
x=-160
for y in range(-160,160+1,20):
    turtle.penup()
    turtle.goto(x,y)
    turtle.pendown()
    turtle.forward(320)
y=160
turtle.right(90)
for x in range(-160,160+1,20):
    turtle.penup()
    turtle.goto(x,y)
    turtle.pendown()
    turtle.forward(320)
turtle.pensize(3)
turtle.color("red")
turtle.speed(0)
turtle.penup()
turtle.goto(0,0)
turtle.pendown()

x=y=0

direction=[0,270,180,90]
list_x=[10,0,-10,0]
list_y=[0,-10,0,10]
r_opposite=[2,3,0,1]
changeNum=3
while(abs(x)<80 and abs(y)<80):
    r=randint(0,3)
    x+=list_x[r]
    y+=list_y[r]
    print(x,y)
    turtle.setheading(direction[r])
    turtle.forward(20)
l
turtle.done()