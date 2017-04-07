# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:43:59 2017

@author: rain
"""

import turtle as tu
import math
multi=30
#-------------x axis---------
tu.penup()
x=-math.pi*3.5
y=0
tu.goto(multi*x,multi*2*y)
tu.pendown()
tu.forward(math.pi*7*multi)
#-----------y axis---------
tu.penup()
x=0
y=-60
tu.goto(x,y)
tu.pendown()
tu.goto(x,-y)
#----------start point------
tu.penup()
x=-math.pi*3.5
y=1
tu.goto(multi*x,multi*2*y)
tu.pendown()
#----------------------


while(x<math.pi*3.5):
    x+=0.1
    y=math.sin(x)
    d=math.cos(x)
    tu.setheading(d*360)
    tu.goto(multi*x,multi*2*y)
    
tu.done()
    