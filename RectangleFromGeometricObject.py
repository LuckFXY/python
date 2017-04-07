# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 21:00:00 2017

@author: rain
"""

from GeometricObject import GeometricObject

class Rectangle(GeometricObject):
    def __init__(self,width=1,height=1):
        super().__init__()
        self.__width=width
        self.__height=height
        
    def getWidth(self):
        return self.__width
    
    def setWidth(self,width):
        self.__width=width
        
    def getHeight(self):
        return self.__height
    
    def setHeight(self,height):
        self.__height=height
        
    def getArea(self):
        return self.__width*self.__height
        
    def getPerimeter(self):
        return 2* (self.__width+self.__height)
