# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 16:52:28 2017

@author: rain
"""

import numpy as np
import cv3

img=np.zeros((3,300,400),dtype=np.uint8)
cv3.imwrite('test.png',img)

