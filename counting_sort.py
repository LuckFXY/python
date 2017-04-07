# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 21:48:26 2017

@author: rain
"""
import random
import numpy as np
#counting sort
def countingSort(Nums):
    length=max(Nums)+1
    count=np.zeros(length,dtype=int)
    for num in Nums:
        count[num]+=1
    print()
    for i in range(1,length):
        count[i]+=count[i-1]
    ret=np.zeros(len(Nums),dtype=int)
    for num in reversed(Nums):
        ret[count[num]-1]=num
        count[num]-=1
    print(list(ret))
        
a=np.random.randint(0,10,size=20)
print(list(a))
countingSort(a)
    