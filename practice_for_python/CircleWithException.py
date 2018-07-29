# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 17:16:46 2017

@author: rain
"""

from GeometricObject import GeometricObject
from math import pi

class Circle(GeometricObject):
    def __init__(self,radius):
        super().__init__()
        self.setRadius(radius)
        
    def getRadius(self):
        return self.__radius
    
    def setRadius(self,radius):
        if radius<0:
            raise RuntimeError("Negative radius")
        else:
            self.__radius=radius
            
    def getArea(self):
        return self.__radius**2*pi
    
    def getDiameter(self):
        return 2*self.__radius
    
    def getPerimeter(self):
        return 2*self.__radius*pi
    
    def printCircle(self):
        print(self.__str__()+" radius: "+ str(self.__radius))
        
        

