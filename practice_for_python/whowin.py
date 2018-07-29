# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 15:28:52 2017

@author: rain
"""

ihash={0:0,2:2,4:4,6:6} #save the best token scheme

def ckATKhash(key,result=-1):
    global ihash
    if key in ihash:
        return ihash[key]
    if result!=-1:
        ihash[key]=result #is Jerry won
    return None
        
def Tom(number):
    
    res=ckATKhash(number)
    if(res!=None and res!=0):
        return True
    
    for i in [2,4,6]:
        num=number-i 
        if(num<0):
            break      
        ret=Jerry(num)
        if ret==False:
            ckATKhash(num,0) #Tom catched Jerry
            return True
    return False #Jerry win
    
def Jerry(number):
    
    res=ckATKhash(number)
    if(res!=None and res!=0):
        return res
    
    for i in [6,4,2]:
        num=number-i 
        if(num<0):
            break
        ret=Tom(num)
        if ret==False: #Tom did not catch Jerry,Jerry win
            ckATKhash(num,i)
            return i
    return False


abhash=dict() #(key:(depth,value))  
def ckabhash(key,depth,value=None):
    global abhash
    if value==None:
        if key in abhash:
            ret=abhash[key] #(depth,value)          
            if ret[0]>=depth:
                return ret[1]
    else:
        abhash[key]=(depth,value)
        return None
    
ACCEPT=1000
DENY=-1000
INFINITE=10000    
def alphabeta(number,depth,alpha,beta):
    if number==0:
        return DENY
    if depth==0 :
        ret=Jerry(number)
        if ret!=False:
            return ACCEPT
        else:
            return number%8 
    v=-INFINITE
    for i in [2,4,6]:
        test=number-i
        if test<0:
            break
        if test==0:
            res=ACCEPT               
        else:
            ckh=ckabhash(test,depth)
            if(ckh!=None):
                res=ckh
            else:
                res=-alphabeta(test,depth-1,-beta,-alpha)
                ckabhash(test,depth,res)
        v=max(v,res)
        alpha=max(alpha,v)
        if beta<=alpha:
            break # beta cut-off
    return v

def computechoose(num):
    lst=[]
    i=Jerry(num)
    if(i!=0):
        return i
    '''
    for i in [2,4,6]:
        if(Jerry(num-i)==False):
            lst.append(i)
    if(len(lst)!=0):
        mini=INFINITE
        ret=lst[0]
        for i in lst:
            res=alphabeta(num-i,3,-INFINITE,INFINITE)
            if res<mini:
                mini=res
                ret=i
        
        return ret
    else:
        print("you win")
        return -1
    '''
#print(Jerry(100))
#a=alphabeta(10,3,-INFINITE,INFINITE)
#print(a)
j=Jerry(100)
print(j)
num=18
while(num!=0):
    userinput=0
    while(userinput not in {2,4,6} or num-userinput<0):
        userinput=eval(input("input the num of balls you pick(2,4,6) : "))
    num-=userinput
    if(num==0):
        print ("you win")
        break
    #n=computechoose(num)
    n=Jerry(num)
    if(n==-1):
        break
    num=num-n
    print("Jerry pick %d balls, total num:%d"%(n,num))
    if(num==0):
        print ("you loss")
        break
    
    
    
    
   