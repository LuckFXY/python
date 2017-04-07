# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 09:28:43 2017

@author: rain
"""

from tkinter import *
import math
from datetime import datetime

class StillClock(Canvas):
    
    isStop=False
    
    def __init__(self,container):
        super().__init__(container)
        self.setCurrentTime()
        self.drawClock()
        
    def getHour(self):
        return self.__hour
    def setHour(self,hour):
        self.__hour=hour
        self.delete("clock")
        self.drawClock()
        
    def getMinute(self):
        return self.__minute
    def setMinute(self,minute):
        self.__minute=minute
        self.delete("clock")
        self.drawClock()
        
    def getSecond(self):
        return self.__second
    def setSecond(self,second):
        self.__second=second
        self.delete("clock")
        self.drawClock()
    def setTime(self,hour,minute,second):
        self.isStop=True
        self.__hour=hour
        self.__minute=minute
        self.__second=second
        self.isStop=False
        self.walk()
    def setCurrentTime(self):
        d=datetime.now()
        self.__hour=d.hour
        self.__minute=d.minute
        self.__second=d.second
    def stopwalk(self):
        self.isStop=True
    def drawClock(self):
        width=float(self["width"])
        height=float(self["height"])
        radius=min(width/2-20,height/2-20)
        secondHandLength=radius*0.8
        minuteHandLength=radius*0.65
        hourHandLength=radius*0.5
        xCenter=width/2
        yCenter=height/2
        self.create_oval(xCenter-radius,yCenter-radius,
                         xCenter+radius,yCenter+radius,
                         tags="clock")
        self.create_text(xCenter-radius+5,yCenter,
                         text="9",tags="clock")
        self.create_text(xCenter+radius-5,yCenter,
                         text="3",tags="clock")
        self.create_text(xCenter,yCenter-radius+5,
                         text="12",tags="clock")
        self.create_text(xCenter,yCenter+radius-5,
                         text="6",tags="clock")
         
        ANGLE_1=2*math.pi/60
        second=self.__second
        xSecond=xCenter+secondHandLength*math.sin(second*ANGLE_1)
        ySecond=yCenter-secondHandLength*math.cos(second*ANGLE_1)
        self.create_line(xCenter,yCenter,xSecond,ySecond,
                         fill="red",tags="clock_walk")
        
        minute=self.__minute
        xMinute=xCenter+minuteHandLength*\
                math.sin((minute+second/60)*ANGLE_1)
        yMinute=yCenter-minuteHandLength*\
                math.cos((minute+second/60)*ANGLE_1)
        self.create_line(xCenter,yCenter,xMinute,yMinute,
                         fill="blue",tags="clock_walk")
                         
        hour=self.__hour%12
        xHour=xCenter+hourHandLength*\
                math.sin((hour+minute/60+second/3600)*ANGLE_1)  
        yHour=yCenter-hourHandLength*\
                math.cos((hour+minute/60+second/3600)*ANGLE_1)                         
                         
        self.create_line(xCenter,yCenter,xHour,yHour,
                         fill="green",tags="clock_walk")
                         
        timestr=str(hour)+":"+str(minute)+":"+str(second)
        self.create_text(xCenter,yCenter+radius-10,
                         text=timestr,tags="clock_walk")
        
    def walk(self):
        width=float(self["width"])
        height=float(self["height"])
        radius=min(width/2,height/2)
        secondHandLength=radius*0.8
        minuteHandLength=radius*0.65
        hourHandLength=radius*0.5
        xCenter=width/2
        yCenter=height/2
        while(self.isStop==False):
            self.__second=self.__second+1
            if(self.__second==60):
                self.__second=0
                self.__minute=self.__minute+1
            if(self.__minute==60):
                self.__minute=0
                self.__hour=(self.__hour+1)%24
            
            self.delete("clock_walk")
            ANGLE_1=2*math.pi/60
            second=self.__second
            xSecond=xCenter+secondHandLength*math.sin(second*ANGLE_1)
            ySecond=yCenter-secondHandLength*math.cos(second*ANGLE_1)
            self.create_line(xCenter,yCenter,xSecond,ySecond,
                             fill="red",tags="clock_walk")
            
            minute=self.__minute
            xMinute=xCenter+minuteHandLength*\
                    math.sin((minute+second/60)*ANGLE_1)
            yMinute=yCenter-minuteHandLength*\
                    math.cos((minute+second/60)*ANGLE_1)
            self.create_line(xCenter,yCenter,xMinute,yMinute,
                             fill="blue",tags="clock_walk")
                             
            hour=self.__hour%12
            xHour=xCenter+hourHandLength*\
                    math.sin((hour+minute/60+second/3600)*ANGLE_1)  
            yHour=yCenter-hourHandLength*\
                    math.cos((hour+minute/60+second/3600)*ANGLE_1)                         
                             
            self.create_line(xCenter,yCenter,xHour,yHour,
                             fill="green",tags="clock_walk")
                             
            timestr=str(hour)+":"+str(minute)+":"+str(second)
            self.create_text(xCenter,yCenter+radius-10,
                             text=timestr,tags="clock_walk")
            self.update()
            self.after(1000)