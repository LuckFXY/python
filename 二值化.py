# -*- coding: utf-8 -*-
"""
Created on Tue May 17 21:14:44 2016

@author: Administrator
"""


import os
import cv2
import numpy as np
import pandas as pd
import pylab as pl



def stdfilt(img, mask):
    n = mask.sum()
    n1 = n - 1
    c1 = cv2.filter2D(img**2, -1, mask / n1, borderType=cv2.BORDER_REFLECT)
    c2 = cv2.filter2D(img, -1, mask, borderType=cv2.BORDER_REFLECT)**2 / (n * n1)
    sig = np.sqrt(np.maximum(c1 - c2, 0))

    return sig
    
def localmean(img, mask):
    lm = cv2.filter2D(
        img, -1, mask / mask.sum(),
        borderType=cv2.BORDER_REPLICATE)

    return lm
 
def img_binary(img, w_size=3, w_sig=0.9, w_lm=0.9):
    if len(img.shape) != 2:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img / 255.0
    mask = np.ones(w_size)

    sig = stdfilt(img, mask)
    if w_lm == 0:
        w_lm = 1
        lm = np.mean(img)
    else:
        lm = localmean(img, mask)

    img = 255 * ((img > sig * w_sig) & (img > w_lm * lm))

    return img
    
s=pd.read_csv('kaggle\\sample.csv')
temp=s.values[0][2:]

 

if __name__ == '__main__':
    #False表示读取为灰度图...
    img=cv2.imread('kaggle\\sample.png',cv2.IMREAD_GRAYSCALE)
    print 'img'
    pl.imshow(img,cmap=pl.get_cmap('gray'))
    pl.show()
    img2 = img_binary(img, w_size=5, w_sig=0.9, w_lm=0.1)
    print 'img2'
    pl.imshow(img2,cmap=pl.get_cmap('gray'))
    pl.show()