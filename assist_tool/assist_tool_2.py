# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:11:23 2017

@author: rain
"""
#for free

from tkinter import Tk,Frame,Canvas,PhotoImage,Radiobutton,Entry,Button,Label,Menu
from tkinter import  IntVar,BooleanVar,StringVar
from tkinter import  LEFT 
from tkinter.filedialog import askdirectory,askopenfilename
from PIL import Image,ImageTk,ImageDraw, ImageFilter
import os
import tkinter.messagebox
import sqlite3
import csv

class MyIO:
    
    def __init__(self,foldername):
        self.index=-1
        self.filelist=[]
        self.len_filelist=0
        if os.path.exists(foldername)==False:
            tkinter.messagebox.showerror("error",("folder: %s does exist")%(foldername))
        self.scan_folder(foldername)
        self.path='mydata.db'
        if os.path.exists(self.path)==False:
            self.createdb()
        
    def scan_folder(self,file_dir):
        for root,dirs,files in os.walk(file_dir):
            for file in files:
                postfix=os.path.splitext(file)[1]
                #print(file,postfix)
                if postfix in {'.bmp','.png','.jpg'}:
                    filename=os.path.join(root,file)
                    self.filelist.append(filename)
        self.len_filelist=len(self.filelist)

    def nextfilename(self):
        if self.index < self.len_filelist-1:
            self.index += 1   
        return self.filelist[self.index]

    def lastfilename(self):
        if self.index !=0:
            self.index -= 1   
        return self.filelist[self.index]
    '''
    while true:
        try:
            x=next(g)
        except StopInteration as e:
            print("generator return value",e.value)
            break
    '''
    def createdb(self):
        if os.path.exists(self.path)==False:
            conn=sqlite3.connect(self.path)
            c= conn.cursor()
            
            c.execute('''
                  CREATE TABLE data
                  (filename text,
                  InCir_D int,InCir_X int, InCir_Y int,
                  OutCir_D int,OutCir_X int, OutCir_Y int)
                  ''')
            #c.execute("INSERT INTO data VALUES ('1.bmp',1,2,3,4,5,6)")
            conn.commit()
            conn.close()
    def setdb_path(self,path):
        self.path=path
    def insertDB(self,filename,block):
        #filename,InCir_D,InCir_X, InCir_Y,OutCir_D,OutCir_X, OutCir_Y=block
        conn=sqlite3.connect(self.path)
        c= conn.cursor()
        block=[filename,]+block
        c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?)",block)
        conn.commit()
        conn.close()
    def updateDB(self,filename,block):
        conn=sqlite3.connect(self.path)
        c= conn.cursor()
        block=block+[filename,]
        c.execute("update data set \
                  InCir_D = ?, \
                  InCir_X = ?, \
                  InCir_Y = ?, \
                  OutCir_D = ?, \
                  OutCir_X = ?, \
                  OutCir_Y = ? \
                  where filename = ?",block)
        conn.commit()
        conn.close()
    def pickoneDB(self,filename):
        conn=sqlite3.connect(self.path)
        c= conn.cursor()
        r=c.execute('select * from data where filename=?',(filename,))
        result=None         
        try:
            result=next(r)
        except StopIteration as e:
            result=None
        finally:
            conn.commit()
            conn.close()
            return result
    def pickallDB(self):
        conn=sqlite3.connect(self.path)
        c= conn.cursor()
        r=c.execute('select * from data ')
        return [i for i in r]
        conn.commit()
        conn.close()
    def processOK(self,filename,block):
        data=self.pickoneDB(filename)
        if data==None:
            self.insertDB(filename,block)
        else:
            self.updateDB(filename,block)
import numpy as np        
class MainWindow:
    
    image_index=0
    ImageCount=0
    canvas=None
    lock=False
    Image_list=[]
    x1,x2,y1,y2=(0,0,0,0)
    
    def autoPositing(self):
        if self.isInnerCircle==True:
            #------------------------
            cw=self.img_org.size[0]//2#width
            ch=self.img_org.size[1]//2 
            r=90
            box=(cw-r,ch-r,cw+r*2,ch+r)
            img_center=self.img_org.crop(box)
            self.canvas.create_rectangle(box)
            #img_center=img_center.filter(ImageFilter.MedianFilter(5))
            img_center=img_center.convert("L")
            #img_center.show()
            w=img_center.size[0] #x
            h=img_center.size[1] #y
            img_center=np.array(img_center)
            small=640*255
            small_x=0
            small_y=0
            for i in range(h):
            
                s=sum(img_center[i,:])
                if s<small:
                    small=s
                    small_y=i
            small=640*255
            for j in range(w):
                s=sum(img_center[:,j])
                if s<small:
                    small=s
                    small_x=j
            #------------------------
            small_x+=cw-r
            small_y+=ch-r
            self.inner_d.set(70)
            self.inner_x.set(small_x)
            self.inner_y.set(small_y)
            print(small,small_x,small_y)
            #-----------------------------   
            self.updateInterface(innercironly=True)
        else:
            self.outside_d.set(self.inner_d.get()+102)
            self.outside_x.set(self.inner_x.get())
            self.outside_y.set(self.inner_y.get())
            self.recovercox()
            self._DrawCircle(moving=False,update=True)
            
                
    def recovercox(self):
        if self.isInnerCircle==True:
            self.x1=self.inner_x.get()-self.inner_d.get()//2
            self.y1=self.inner_y.get()-self.inner_d.get()//2
            self.x2=self.inner_x.get()+self.inner_d.get()//2
            self.y2=self.inner_y.get()+self.inner_d.get()//2
        else:
            self.x1=self.outside_x.get()-self.outside_d.get()//2
            self.y1=self.outside_y.get()-self.outside_d.get()//2
            self.x2=self.outside_x.get()+self.outside_d.get()//2
            self.y2=self.outside_y.get()+self.outside_d.get()//2
    def updateInterface(self,block=None,innercironly=False):
        self.lock=False
        index=0
        if block!=None:
            for vi in self.variable_list[1:]:
                vi.set(block[index])
                index+=1       
        self.isInnerCircle=True
        self.recovercox()
        self._DrawCircle(moving=False,update=True)
        if innercironly==False:
            self.isInnerCircle=False
            self.recovercox()
            self._DrawCircle(moving=False,update=True)
        self.canvas.update()
        #---------------------
        self.processChooseInner()
    def autoTurn(self):
        
        data='start'
        count=0
        pic_num=self.myio.len_filelist
        while(data!=None and count<pic_num):
            count+=1
            self.processRButton()
            data=self.myio.pickoneDB(self.filename)
    def processRButton(self):
        self.lock=False
        self.filename=self.myio.nextfilename()
        self.showPicture(self.filename)
        self.currentfile.set(self.filename)
        
        data=self.myio.pickoneDB(self.filename)
        #print(data)
        if data!=None:
            self.updateInterface(data[1:])
        else:
            self.processChooseInner()
            self.autoPositing()
            
        
    def processLButton(self):
        self.lock=False
        filename=self.myio.lastfilename()
        self.showPicture(filename)
        self.currentfile.set(filename)
        data=self.myio.pickoneDB(filename)
        if data!=None:
            self.updateInterface(data[1:])
        
    def processChooseInner(self):
        self.radio_innerCircle.select()
        self.radio_outsideCircle.deselect()
        self.isInnerCircle=True
        self.recovercox()
    def processChooseOutside(self):
        self.radio_innerCircle.deselect()
        self.radio_outsideCircle.select()
        self.isInnerCircle=False
        self.autoPositing()
        
    def processOk(self):

        filename=self.currentfile.get()
        block=[vi.get() for vi in self.variable_list[1:]]
        self.myio.processOK(filename,block)
        #--------------draw a circle-------
        idraw=ImageDraw.Draw(self.img_org)
        r=block[0]//2
        x=block[1]
        y=block[2]    
        innercirobx=[x-r,y-r,x+r,y+r]
        r=block[3]//2
        x=block[4]
        y=block[5]   
        outsidecirobx=[x-r,y-r,x+r,y+r]
        for i in range(2):
            idraw.ellipse(innercirobx,outline='white')
            innercirobx=self.inc_r(innercirobx)
            idraw.ellipse(outsidecirobx,outline='white')
            outsidecirobx=self.inc_r(outsidecirobx)
        
        outputname='output_image/'+os.path.split(self.currentfile.get())[-1]
        print(outputname)
        self.img_org.save(outputname)
            #----------------------------------
        self.processRButton()
    
    def Press(self,event):

        self.x1=event.x
        self.y1=event.y
    def showPicture(self,filename):

        self.img_org=Image.open(filename)
        self.img=ImageTk.PhotoImage(self.img_org)
        self.h=self.img.height()
        self.w=self.img.width()
        if self.canvas.find_withtag('img'):
            self.canvas.delete('img')       
        self.canvas.create_image(self.w//2,self.h//2,image=self.img)
        self.canvas.update()

        
    def _DrawCircle(self,moving=True,update=False):

        ch='inner'
        if self.isInnerCircle== False:
            ch='outside'
        if update:
            self.canvas.delete(ch)
        d=self.x2-self.x1
        if not self.canvas.find_withtag(ch):
            self.canvas.create_oval(
                self.x1,self.y1,self.x1+d,self.y1+d,
                outline='white',tags=ch,width=2)
        elif moving:
            self.canvas.delete(ch)
            
        if self.isInnerCircle:
            self.inner_d.set(d)
            self.inner_x.set(self.x1+d//2)
            self.inner_y.set(self.y1+d//2)
        else:
            self.outside_d.set(d)
            self.outside_x.set(self.x1+d//2)
            self.outside_y.set(self.y1+d//2)

    def Release(self,event):
        self._DrawCircle(moving=False,update=True)
    def Draw(self,event):
        self.x2=event.x
        self.y2=event.y
        self._DrawCircle()
    def PressKey(self,event):
       key=event.keysym
       if self.lock==False:
           self.lock=True
           self.recovercox()
       if key=='w':
           self.y1-=2
           self.y2-=2
       elif key=='s' :
           self.y1+=2
           self.y2+=2
       elif key=='a' :
           self.x1-=2
           self.x2-=2
       elif key== 'd':
           self.x1+=2
           self.x2+=2
           
       elif key =='q':
           self.x2-=2
           self.y2-=2
       elif key =='e':
           self.x2+=2
           self.y2+=2
       elif key =='space':
           if self.isInnerCircle==True:
               self.processChooseOutside()
           else:
               self.processOk()
               
               
       self._DrawCircle(moving=False,update=True)
           
           
    def openFolder(self):
        filenameforReading=askdirectory()
        self.myio=MyIO(filenameforReading)
        
        #self.processRButton()
        self.autoTurn()
    def openCsv(self):
        tkinter.messagebox.showerror("error","under construction")
    
    def openDatabase(self):
        filenameforReading=askopenfilename()
        if self.myio==None:
            self.myio=MyIO(filenameforReading)
        else:
            self.myio.setdb_path(filenameforReading)
        
    def outputcsv(self):
        data=self.myio.pickallDB()
        outputname='data.csv'
        with open(outputname,'a+') as csvfile:
            f_csv=csv.writer(csvfile)
            for row in data:
                f_csv.writerow(row)
                
    def inc_r(self,box):
        r=[-1,-1,1,1]
        for i in range(4):
            box[i]+=r[i]
        return box
            
    def outputpic(self):
        data=self.myio.pickallDB()
        for row in data:
            #--------------draw a circle-------
            
            self.img_org=Image.open(row[0])
            idraw=ImageDraw.Draw(self.img_org)
            r=row[1]//2
            x=row[2]
            y=row[3]    
            innercirobx=[x-r,y-r,x+r,y+r]
            r=row[4]//2
            x=row[5]
            y=row[6]   
            outsidecirobx=[x-r,y-r,x+r,y+r]
            for i in range(2):
                idraw.ellipse(innercirobx,outline='white')
                innercirobx=self.inc_r(innercirobx)
                idraw.ellipse(outsidecirobx,outline='white')
                outsidecirobx=self.inc_r(outsidecirobx)
            
            outputname='output_image/'+os.path.split(row[0])[-1]
            print(outputname)
            self.img_org.save(outputname)
            #----------------------------------
        
    def __init__(self):
        
        self.myio=None

        window=Tk()
        window.title("Assist Tool")       
        leftICO=PhotoImage(file="ICO/left.gif")
        rightICO=PhotoImage(file="ICO/right.gif")
        okICO=PhotoImage(file="ICO/ok.gif")
        self.inner_x=IntVar()
        self.inner_y=IntVar()
        self.inner_d=IntVar()
        self.outside_x=IntVar()
        self.outside_y=IntVar()
        self.outside_d=IntVar()
        self.currentfile=StringVar()
        self.variable_list=[
            self.currentfile,
            self.inner_d,
            self.inner_x,
            self.inner_y,
            self.outside_d,
            self.outside_x,
            self.outside_y           
        ]
        self.h=480
        self.w=640
        self.isInnerCircle=BooleanVar()
        self.isInnerCircle.set(True)
        
        frame_left=Frame(window)
        frame_left.grid(row=1,column=1)
        frame_right=Frame(window)
        frame_right.grid(row=1,column=2)
        frame_bottom=Frame(window)
        frame_bottom.grid(row=2,column=1)
        frame_right_1=Frame(frame_right)
        frame_right_1.grid(row=1,column=1)
        frame_right_2=Frame(frame_right)
        frame_right_2.grid(row=2,column=1)
        frame_right_3=Frame(frame_right)
        frame_right_3.grid(row=3,column=1)
        frame_right_4=Frame(frame_right)
        frame_right_4.grid(row=4,column=1)
        frame_right_5=Frame(frame_right)
        frame_right_5.grid(row=5,column=1)
        
        #------------------banging---------
        self.canvas=Canvas(frame_left)        
        self.canvas["width"]=self.w
        self.canvas["height"]=self.h
        self.canvas.pack()
        self.canvas.bind('<Button-1>',self.Press)
        self.canvas.bind('<B1-Motion>',self.Draw)
        self.canvas.bind('<ButtonRelease-1>',self.Release)
        window.bind('<Key>',self.PressKey)
        
        #-------------show background picture-----

        self.showPicture("ICO/rabbit640480.jpg")
        
        #--------------show filename 
        self.label_filename=Label(frame_bottom,textvariable=self.currentfile)
        self.label_filename.pack()  
        #-------------control button
        Button(frame_right_2,image=leftICO,
               command=self.processLButton).pack(side=LEFT)
        Button(frame_right_2,image=rightICO,
               command=self.processRButton).pack(side=LEFT)
        #-------------show info of inner circle
        
        self.radio_innerCircle=Radiobutton(frame_right_3,text="Inner Circle",
            command=self.processChooseInner,variable=self.isInnerCircle,value=True)
        self.radio_innerCircle.grid(row=1,column=2)
        Label(frame_right_3,text="d").grid(row=2,column=1)
        self.entry_inner_d=Entry(frame_right_3,textvariable=self.inner_d)
        self.entry_inner_d.grid(row=2,column=2)
        Label(frame_right_3,text="x").grid(row=3,column=1)
        self.entry_inner_x=Entry(frame_right_3,textvariable=self.inner_x)
        self.entry_inner_x.grid(row=3,column=2)
        Label(frame_right_3,text="y").grid(row=4,column=1)
        self.entry_inner_y=Entry(frame_right_3,textvariable=self.inner_y)
        self.entry_inner_y.grid(row=4,column=2)
        #------------show info of outside circle
        self.radio_outsideCircle=Radiobutton(frame_right_4,text="Outside Circle",
            command=self.processChooseOutside,variable=self.isInnerCircle,value=False)
        self.radio_outsideCircle.grid(row=1,column=2)        
        Label(frame_right_4,text="d").grid(row=2,column=1)
        self.entry_outside_d=Entry(frame_right_4,textvariable=self.outside_d)
        self.entry_outside_d.grid(row=2,column=2)
        Label(frame_right_4,text="x").grid(row=3,column=1)
        self.entry_outside_x=Entry(frame_right_4,textvariable=self.outside_x)
        self.entry_outside_x.grid(row=3,column=2)
        Label(frame_right_4,text="y").grid(row=4,column=1)
        self.entry_outside_y=Entry(frame_right_4,textvariable=self.outside_y)
        self.entry_outside_y.grid(row=4,column=2)        
        #-------------ok button
        Button(frame_right_5,image=okICO,
               command=self.processOk).pack(side=LEFT)
        #--------------menubar
        menubar=Menu(window)
        window.config(menu=menubar)
        openMenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Open",menu=openMenu)
        openMenu.add_command(label="Folder",command=self.openFolder)     
        openMenu.add_command(label="sqlite3 database",command=self.openDatabase)
        openMenu.add_command(label="csv file",command=self.openCsv)
        
        outputMenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Output",menu=outputMenu)
        outputMenu.add_command(label="csv file",command=self.outputcsv)
        outputMenu.add_command(label="picture",command=self.outputpic)

        #-------------finally---------     
        
        self.radio_innerCircle.select()
        if os.path.exists('output_image')==False:
            os.mkdir('output_image')
        window.mainloop()
if __name__=='__main__':        
	MainWindow()
