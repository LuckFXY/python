# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 17:45:42 2017

@author: rain
"""
class GeometricObject:
    def __init__(self,color="green",filled=True):
        self.__color=color
        self.__filled=filled
        
    def getColor(self):
        return self.__color
    
    def setColor(self,color):
        self.__color=color
        
    def isFilled(self):
        return self.__filled
        
    def setFilled(self,filled):
        self.__filled=filled
        
    def __str__(self):
        return "color: "+self.__color+'\n'\
               "and filled: " + str(self.__filled)
               
