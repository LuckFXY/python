# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 09:43:26 2017

@author: rain
"""
import numpy as np

a=np.array(range(1,10)).reshape(3,3)
b=np.array(range(10,19)).reshape(3,3)
def multiplyMatrix(a,b):
    if(a.shape[1]!=b.shape[0]):
        print("the size of matrix is illegal ")
        print("a.size="+a.shape)
        print("b.size="+b.shape)
        return None
    c=np.zeros((a.shape[0],b.shape[1]),dtype=float)
    for row in range(a.shape[0]):
        for aj in range(a.shape[0]):
            for bj in range(a.shape[1]):
                c[row][bj]+=a[row,aj]*b[aj,bj]
    return c
    
c=multiplyMatrix(a,b)
print (c)
    