# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 09:40:46 2017

@author: rain
"""
def printRange(myrange_list,title=None):
    if title!=None:
        print(title)
    print('/-----------------------------------------\\')
    length_list=[len(mr) for mr in myrange_list]
    length=length_list[0]
    assert min(length_list)==max(length_list)
    epoch=length//10
    if epoch!=(length/10.0):
        epoch+=1
    i=0
    while i<epoch:    
        high=(i+1)*10
        if high>=len(mr) :
            high=len(mr)
        for mr in myrange_list:          
            for j in range(i*10,high):      
                print(("%3d") % (mr[j])),
            print('\n')
        i+=1
    print('\\-----------------------------------------/')
#work out the prime number table
import numpy as np
NUMBER=200
myrange=np.array(range(NUMBER))
isprime=np.ones(NUMBER,dtype=np.int8)
primetable={}
isprime[0:2]=0
index=0
for num in range(2,NUMBER):
    if isprime[num]==1: # prime tags is true
        primetable[num]=index
        index+=1
        for i in range(num+num,NUMBER,num):
            isprime[i]=0
            if isprime[myrange[i]]==0:
                myrange[i]/=num
                    
#get prime number talbe
primetable_keys=primetable.keys()
printRange([primetable_keys],"the parme number table")

#calculate the poistion of the maximum prime factor of a number in the prime table
PM=[]
NUM_LIST=range(2,NUMBER)
for num in NUM_LIST:
    testnum=num
    if isprime[testnum]!=1:
        testnum=myrange[testnum]
        while isprime[testnum]!=1: #reverse find prime factor of a given number
            testnum=myrange[testnum]
            
    PM.append(primetable[testnum])

printRange([NUM_LIST,PM],
           "the poistion of the maximum prime factor of a number in the prime table")