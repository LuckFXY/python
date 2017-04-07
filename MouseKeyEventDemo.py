# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:00:35 2017

@author: rain
"""

from tkinter import *
import numpy as np
class MouseKeyEventDemo:
    point=np.array([[0,0],[0,0]])
    def __init__(self):
        window=Tk()
        window.title("Event Demo")
        f1=Frame(window,width=600,height=400)
        f1.grid(row=1,column=1)
        img=PhotoImage(file="image/rabbit.gif")
        canvas=Canvas(f1,bg="white",width=600,height=400)
        canvas.pack()
        cx=img.width() / 2.0
        cy=img.height() / 2.0
        canvas.create_image(cx,cy,image=img)
        #Bind with <Button-1> event
        canvas.bind("<ButtonPress-1>",self.processMousePressEvent)
        canvas.bind("<ButtonRelease-1>",self.processMouseReleaseEvent)
        
        f2=Frame(window,width=600,height=400)
        f2.grid(row=1,column=1)
        ca=Canvas(f2,bg="white",width=600,height=400)
        ca.pack()
        ca.create_image(width//2,height//2, image=photoimg) 
        window.mainloop()
        
    def processMousePressEvent(self,event):
        self.point[0]=(event.x,event.y)
        #print("click at",point)
    
    def processMouseReleaseEvent(self,event):
        self.point[1]=(event.x,event.y)
        print(self.point[0],self.point[1])
        
    
MouseKeyEventDemo()