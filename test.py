# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import pylab as pl

#train=pd.read_csv('kaggle\\train.csv')
#s=train[0:12]
#s.to_csv('kaggle\\sample.csv')
s=pd.read_csv('kaggle\\sample.csv')
#temp=s.values[0]

'''
for index,row in s.iterrows():
    
    key=row['label']
    print 'it is:' + str(key)
    data=np.array(row[2:]).reshape((28,28))
    pl.imshow(data,cmap=plt.get_cmap('gray'))
    pl.show()
    #raw_input('press enter to continue')
'''
#x=range(temp.shape[0])
#y=temp
#pl.plot(x,y,'o')

#pl.hist(temp)
def img_binary(image,threshhold):
    for i in range(28):
        for j in range(28):
            if image[i][j]>threshhold:
                image[i][j]=255
            else :
                image[i][j]=0
    return image

def img_inverse(image):
    for i in range(28):
        for j in range(28):
            image[i][j]=abs(image[i][j]-255)
    return image
 '''   
for index,row in s.iterrows():
    key=row['label']
    data=np.array(row[2:]).reshape((28,28))
    pl.subplot(4,3,index)
    pl.imshow(data,cmap=pl.get_cmap('gray'))
pl.show()    

for index,row in s.iterrows():
    key=row['label']
    data=np.array(row[2:]).reshape((28,28))
    data=img_binary(data,50)
    pl.subplot(4,3,index)
    pl.imshow(data,cmap=pl.get_cmap('gray'))
pl.show()  
  
for index,row in s.iterrows():
    key=row['label']
    data=np.array(row[2:]).reshape((28,28))
    data=img_binary(data,50)
    data=img_inverse(data)
    pl.subplot(4,3,index)
    pl.imshow(data,cmap=pl.get_cmap('gray'))
pl.show()    
'''