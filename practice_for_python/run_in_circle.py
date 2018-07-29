# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 11:14:19 2017

@author: rain
"""

import turtle as tu
from math import atan,pi,sqrt,acos,sin,cos
R=200
tu.penup()
tu.goto(0,-R)
tu.pendown()
tu.circle(R)
tu.speed(0)

sp=(0,R/2)
tu.penup()
tu.goto(sp)
#tu.setheading(240)
tu.pendown()

count=0
x=tu.xcor()
y=tu.ycor()
x_2=x**2
y_2=y**2
R_2=R*R
rp_cor=sp
lock=False
reflect=0
while(count<9):
    step=R_2/(x_2*10+y_2*10+R_2)*10
    x_try=x+step*cos(reflect)
    y_try=y+step*sin(reflect)
    #tu.forward(R_2/(x_2*10+y_2*10+R_2)*2)
    #x=tu.xcor()
    #y=tu.ycor()
    x_2=x_try**2
    y_2=y_try**2
    if(x_2+y_2<R_2):
        x=x_try
        y=y_try
        tu.goto(x,y)
    else:

        dx=x-rp_cor[0]
        dy=y-rp_cor[1]
        ds=sqrt(dx**2+dy**2)
        print("x=%f,y=%f"%(x,y))
        print("dx=%f,dy=%f,ds=%f,l=%f"%(dx,dy,ds,x_2+y_2))      
        
        alpha=acos(abs(x)/R)
        beta=acos(abs(dx)/ds)
        theta=abs(beta-alpha)
        #print("theta=%f,alpha=%f"%(theta,alpha))

        #if(dx>0 and dy>0):
        if(x<0 and y>0):
            alpha=pi-alpha
        elif(x<0 and y<0):
            alpha=pi+alpha
        elif(x>0 and y<0):
            alpha=-alpha  
        if ((dx*x+dy*y)/(ds*R)<0):    
            reflect=alpha+(pi-theta)
        else:
            reflect=alpha-(pi-theta)
        [alpha2,beta2,theta2]=[i/pi*180 for i in (alpha,beta,theta)]
        print("alpha=%f,beta=%f,theta=%f"%(alpha2,beta2,theta2),end=',')
        print("reflect=%f"%(reflect))
        #tu.setheading(reflect)
        
        rp_cor=(x,y)
        print("rp_cor=%f,%f\n"%(x,y))        
        while(False and x_2+y_2>R_2):
            step=0.001
            x=x+step*cos(reflect)
            y=y+step*sin(reflect)
            tu.goto(x,y)
            x_2=x**2
            y_2=y**2
            #print(x,y)
            print(".",end='')
        count+=1
        
    
    
tu.done()
