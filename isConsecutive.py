# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 10:24:00 2017

@author: rain
"""

#if the list contains four consecutive numbers with the same value reutrn true

import numpy as np
import random
'''
a=[i for i in range(9)]*9
random.shuffle(a)
matrix=np.array(a).reshape(9,9)
'''
"""
the 6 type of adjacent
1 1|1 0|0 0|0 1|1 0|0 1| 
0 0|1 0|1 1|0 1|0 1|1 0|
 1   2   3   4   5   6
"""
matrix=np.array(
      [[8, 6, 1, 1, 1, 1, 8, 8, 0],
       [4, 6, 1, 6, 5, 5, 4, 4, 1],
       [2, 2, 6, 3, 2, 5, 6, 4, 0],
       [2, 3, 2, 0, 7, 6, 5, 4, 0],
       [2, 4, 1, 4, 6, 8, 1, 4, 8],
       [2, 0, 8, 6, 1, 5, 7, 3, 1],
       [7, 8, 7, 5, 2, 6, 4, 8, 6],
       [2, 4, 6, 7, 0, 3, 3, 3, 3],
       [1, 3, 2, 7, 7, 2, 7, 5, 3]])
       

'''
def isEqual_1(matrix,m,n,res2,multi=2):
    H=matrix.shape[0]
    W=matrix.shape[1]
    if m<0 or n<0 or m>=H or n>=W:
        return 0
    else:
        return 1 if res2==matrix[m,n] else 0
def findAdjacent(matrix):
    
    aim   :search adjacent number in trad(2*2)
    input :matrix
    ouput :
        type6 is a list of coordinate which belong to the same type
        list:[(the type of adjacent,adjacent value),...]
    
    type_m=[[],[],[],[],[],[],[],[]]
    type_n=[[],[],[],[],[],[],[],[]]
    type6_mn=[type_m,type_n]

    conn34=[[],[]]
    H=matrix.shape[0]//2
    W=matrix.shape[1]//2  
    for m in range(H):
        for n in range(W):
            a=matrix[m*2,n*2]  # |a b|
            b=matrix[m*2,n*2+1]# |c d|
            c=matrix[m*2+1,n*2]
            d=matrix[m*2+1,n*2+1]

            if(a==b):
                type_m[1].append(m)
                type_n[1].append(n)                
                num=isEqual_1(matrix,m*2,n*2-1,a)+\
                    isEqual_1(matrix,m*2,n*2+2,a)
                if num!=0:
                    conn34[num-1].append((m,n))

            if(a==c):
                type_m[2].append(m)
                type_n[2].append(n)
                num=isEqual_1(matrix,m*2-1,n*2,a)+\
                    isEqual_1(matrix,m*2+2,n*2,a)
                if num!=0:
                    conn34[num-1].append((m,n))

            if(a==d):
                type_m[5].append(m)
                type_n[5].append(n)
                num=isEqual_1(matrix,m*2-1,n*2-1,a)+\
                    isEqual_1(matrix,m*2+2,n*2+2,a)
                if num!=0:
                    conn34[num-1].append((m,n))

            if(d==c):
                type_m[3].append(m)
                type_n[3].append(n)
                num=isEqual_1(matrix,m*2+1,n*2-1,d)+\
                    isEqual_1(matrix,m*2+1,n*2+2,d)
                if num!=0:
                    conn34[num-1].append((m,n))
                    
            if(d==b):
                type_m[4].append(m)
                type_n[4].append(n)
                num=isEqual_1(matrix,m*2-1,n*2+1,d)+\
                    isEqual_1(matrix,m*2+2,n*2+1,d)
                if num!=0:
                    conn34[num-1].append((m,n))
                    
            if(b==c):
                type_m[6].append(m)
                type_n[6].append(n)
                num=isEqual_1(matrix,m*2-1,n*2+2,b)+\
                    isEqual_1(matrix,m*2+2,n*2-1,b)
                if num!=0:
                    conn34[num-1].append((m,n))
                    
    print(type6_mn)
    print(conn34[0])
    print("4",conn34[1])
    return type6_mn,conn34  

findAdjacent(matrix)
'''
def maxAdjacentNum(matrix,m,n,m2,n2):
    #up,down,left,right,up-left,down-left
    if m==m2 and n==n2:
        return 0
    dm=m2-m
    dn=n2-n
    H=matrix.shape[0]
    W=matrix.shape[1]
    key=matrix[m,n]
    m2=m+dm
    n2=n+dn
    num=0
    
    while(0<=m2<H and 0<=n2<W and matrix[m2,n2]==key):
       m2=m2+dm
       n2=n2+dn
       num+=1
    if num==0:
        return 0
    m2=m-dm
    n2=n-dn
    while(0<=m2<H and 0<=n2<W and matrix[m2,n2]==key):
       m2=m2-dm
       n2=n2-dn
       num+=1
    return num+1
def getvalue(lst):
    return lst[0]
def try1(matrix):
    print(matrix)
    H=matrix.shape[0]
    W=matrix.shape[1]
    m8=np.zeros((H,W))
    hotpoint=[[],[],[],[]] ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for m in range(1,H-1):
        for n in range(1,W-1):
            key=matrix[m,n]
            num=-1
            for i in range(m-1,m+2):
                for j in range(n-1,n+2):
                    num+=1 if key==matrix[i,j] else 0
            if(num!=0):
                hotpoint[num].append((m,n))
            m8[m,n]=num
    for m in (0,H-1):
        for n in range(H-1):
            key=matrix[m,n]
            num=-1
            for i in range(m-1,m+2):
                if 0<=i<H:
                    for j in range(n-1,n+2):
                         if 0<=j<W:
                            num+=1 if key==matrix[i,j] else 0
            if(num!=0):
                hotpoint[num].append((m,n))
            m8[m,n]=num
    for n in (0,W-1):
        for m in range(1,H-1):
            key=matrix[m,n]
            num=-1
            for i in range(m-1,m+2):
                if 0<=i<H:
                    for j in range(n-1,n+2):
                         if 0<=j<W:
                            num+=1 if key==matrix[i,j] else 0
            if(num!=0):
                hotpoint[num].append((m,n))
            m8[m,n]=num
            
            
    print(m8)
    #hotpoint.sort(key=getvalue)
    print("h3:",hotpoint[3])
    return m8,hotpoint

#try1(matrix)
def test(matrix):
    H=matrix.shape[0]
    W=matrix.shape[1]
    m8,hotpoint=try1(matrix)
    for cor in hotpoint[3]:
        m,n=cor
        for i in range(m-1,m+2):
            if 0<=i<H:
                for j in range(n-1,n+2):
                    if 0<=j<W:
                        if m8[i,j]!=0:
                            num=maxAdjacentNum(matrix,m,n,i,j)
                            print("cor=",(m,n),"num=",num)
            
test(matrix)