# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 16:56:02 2017

@author: rain
"""

from tkinter import *
class ImageDemo:
    
    image_index=0
    ImageCount=0
    canvas=None
    Image_list=[]
    def processLButton(self):
        self.image_index=(self.image_index+self.ImageCount-1)%self.ImageCount
        self.canvas.create_image(120,240,image=self.Image_list[self.image_index])
   
    def processRButton(self):
        self.image_index=(self.image_index+1)%self.ImageCount
        self.canvas.create_image(120,240,image=self.Image_list[self.image_index])
        
        
    def __init__(self):
        
        window=Tk()
        window.title("Image Demo")
        ximage=PhotoImage(file="image/x.gif")
        oimage=PhotoImage(file="image/o.gif")
        leftimage=PhotoImage(file="image/left.gif")
        rightimage=PhotoImage(file="image/right.gif")
        self.Image_list=[]
        ImageName_list=["hawk","rabbit","bear"]
        self.ImageCount=len(ImageName_list)
        for i in range(len(ImageName_list)):
            path="image/%s.gif"%(ImageName_list[i])
            print(path)
            image=PhotoImage(file=path)
            self.Image_list.append(image)
        
        frame1=Frame(window)
        frame1.pack()
        Label(frame1,image=self.Image_list[self.image_index]).pack(side=LEFT)
        self.canvas=Canvas(frame1)
        self.canvas.create_image(120,240,
               image=self.Image_list[(self.image_index+1)%self.ImageCount])
        self.canvas["width"]=400
        self.canvas["height"]=600
        self.canvas.pack(side=LEFT)
        
        frame2=Frame(window)
        frame2.pack()
        Button(frame2,image=leftimage,
               command=self.processLButton).pack(side=LEFT)
        Button(frame2,image=rightimage,
               command=self.processRButton).pack(side=LEFT)
        Radiobutton(frame2,image=ximage).pack(side=LEFT)
        Radiobutton(frame2,image=oimage).pack(side=LEFT)
        
        window.mainloop()
         
ImageDemo()