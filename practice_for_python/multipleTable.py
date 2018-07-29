# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 18:49:46 2017

@author: rain
"""
tablename="MultiplicationTable"
numOfBlank=50
def printline(length,content=''):
    assert type(content)==str
    assert type(length)==int
    numOfBlank=length-len(content)
    flag=numOfBlank%2==1
    numOfBlank=numOfBlank//2
    for i in range(numOfBlank):
        print('-',end='')
    print(content,end='')
    if flag:
        print(' ',end='')
    for i in range(numOfBlank):
        print('-',end='')
    print()    
    
    
printline(numOfBlank,tablename)    
print("   ",end='')    
for j in range(1,10):
    print(format(j,"5d") , end='')
print()
printline(numOfBlank)
for i in range(1,10):
    print(i,'|',end='')
    for j in range(1,10):
        print(format(i*j,"5d"),end='')
    print()
printline(numOfBlank)