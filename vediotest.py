# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 09:48:08 2017

@author: rain
"""

import cv2

clicked =False
def onMouse(event,x,y,flags,param):
    global clicked
    if event==cv2.EVENT_LBUTTONUP:
        clicked=True
        
        
cv2.namedWindow("MyWindow")
cv2.setMouseCallback("MyWindow",onMouse)

cap=cv2.VideoCapture(0)
if not cap.isOpened(): 
    print('Capture failed because of camera')
else:
    success,frame=cap.read()
    while success and cv2.waitKey(10) !=27 and not clicked:
        cv2.imshow("MyWindow",frame)
        success,frame=cap.read()
    
cv2.destroyWindow("MyWindow")
cap.release()