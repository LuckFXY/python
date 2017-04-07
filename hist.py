# -*- coding: utf-8 -*-
"""
Created on Sat May 14 16:08:55 2016

@author: Administrator
"""

import cv2      
import numpy as np  

image = cv2.imread("kaggle\sample.png", 0)  
hist = cv2.calcHist([image],  
    [0], #使用的通道  
    None, #没有使用mask  
    [256], #HistSize  
    [0.0,255.0]) #直方图柱的范围 
    
hist= cv2.calcHist([image], [0], None, [256], [0.0,255.0])    
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)    
histImg = np.zeros([256,256,3], np.uint8)    
hpt = int(0.9* 256);    
color=[255,0,0]      
for h in range(256):    
    intensity = int(hist[h]*hpt/maxVal)    
    cv2.line(histImg,(h,256), (h,256-intensity), color)    
cv2.imshow("histImg", histImg)   
cv2.imshow("Img", image)
cv2.waitKey(0)   
cv2.destroyAllWindows()