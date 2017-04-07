# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 22:05:32 2017

@author: rain
"""

from random import randint

def getRandomCharacter(ch1,ch2):
    return chr(randint(ord(ch1),ord(ch2)))
    
def getRandomLowerCaseLetter():
    return getRandomCharacter('a','z')

def getRandomUpperCaseLetter():
    return getRandomCharacter('A','Z')
    
def getRandomDigitCharacter():
    return getRandomCharacter('0','9')
    
def getRandomASCIICharacter():
    return chr(randint(0,127))
    
    
def test(getRandomCharacter_func):    
    print('----------------------------------------')
    for i in range(1,128):  
        ch=getRandomCharacter_func()
        print(ch,end='')
        if i%30==0:
            print()
    print()
func_list={
    0:getRandomLowerCaseLetter,
    1:getRandomUpperCaseLetter,
    2:getRandomDigitCharacter,
    3:getRandomASCIICharacter}
   
for i in range(4):
    test(func_list[i])
          
