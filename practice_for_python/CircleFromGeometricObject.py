# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 20:45:25 2017

@author: rain
"""

from GeometricObject import GeometricObject
from math import pi

class Circle(GeometricObject):
    def __init__(self,radius):
        super().__init__()
        self.__radius=radius
    
    def getRadius(self):
        return self.__radius
        
    def setRadius(self,radius):
        self.__radius=radius
        
    def getArea(self):
        return self.__radius*self.__radius*pi
        
    def getDiameter(self):
        return 2*self.__radius
        
    def getPerimeter(self):
        return 2*self.__radius*pi
        
    def printCircle(self):
        print(self.__str__()+" radius: "+str(self.__radius))
        
