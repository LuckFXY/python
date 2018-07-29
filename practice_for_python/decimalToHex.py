# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 20:25:00 2017

@author: rain
"""

def decimalToHex(decimalValue):
    symbol='0123456789ABCDEF'
    result=[]
    while(decimalValue>=16):  
        remainder=decimalValue%16
        decimalValue=decimalValue//16        
        #print(remainder)
        result.append(symbol[remainder])
    result.append(symbol[decimalValue])
    result.reverse()
    res=''.join(str(i) for i in result)
    print (res)
    return res
    

decimalToHex(4095)
