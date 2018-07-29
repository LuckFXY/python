# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 21:00:00 2017

@author: rain
"""

from CircleFromGeometricObject import Circle
from RectangleFromGeometricObject import Rectangle

def displayObject(g):
    print("Area is ",g.getArea())
    print("perimeter is",g.getPerimeter())
    if isinstance(g,Circle):
        print("Diameter is",g.getDiameter())
    elif isinstance(g,Rectangle):
        print("Width is ",g.getWidth())
        print("Height is ",g.getHeight())
if __name__=="__main__":
    circle=Circle(1.5)
    #print("A circle",circle)
    rectangle=Rectangle(2,4)
    #print("\nA rectangle",rectangle)
    print("circle")
    displayObject(circle)
    print("rectangle")
    displayObject(rectangle)