# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:35:06 2017

@author: rain
"""

import numpy as np
import pylab as pl
import pickle

with open("draw_row_test1_data.pickle","rb") as f:
    data=pickle.load(f)
#print (data)
data=data[np.argsort(data[:,1])[::-1]]
TAGS=[0,1]
def getpredtag(probability,threashold=0.5):
    if probability>=threashold:
        return TAGS[0]
    else:
        return TAGS[1]
def confusion_matrix(_data,threashold=0.5):
    table=np.zeros((2,2),dtype=int)
    for d in _data:
        row=getpredtag(d[1],threashold) #prediction
        column=int(d[0]) #real tags
        table[row,column]+=1
    return table
def calculate_rocxy(_data,threshold):
    cm=confusion_matrix(_data,threshold)
    TP=cm[0,0]
    FP=cm[0,1]
    FN=cm[1,0]
    TN=cm[1,1]
    TPR=TP/(TP+FN) 
    FPR=FP/(TN+FP)
    return (FPR,TPR)

def mydraw(plot_data,xlabel,ylabel):
    pl.plot(plot_data[:,0],plot_data[:,1],label='roc')
    pl.title('FPR-TPR')
    pl.xlabel=xlabel
    pl.ylabel=ylabel
    pl.legend(loc='upper right')
    pl.show()

   
threshold_list=data[:,1]
plot_data=np.zeros((len(threshold_list),2))
i=0
for threshold in threshold_list:
    plot_data[i]=calculate_rocxy(data,threshold)#(FPR,TPR)
    #print(plot_data[i])
    i+=1
    
mydraw(plot_data,'False positive rate','True positive rate')
    
    
    