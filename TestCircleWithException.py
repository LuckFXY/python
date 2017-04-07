# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 17:25:21 2017

@author: rain
"""

from CircleWithException import Circle

try:
    radius_list=[5,0,-5]
    for i in range(len(radius_list)):       
        c=Circle(radius_list[i])
        print("c%d's area is %f"%(i,c.getArea()))
except RuntimeError:
    print("Invalid radius")