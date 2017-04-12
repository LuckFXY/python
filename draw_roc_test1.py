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
print('\tLabel\tProbability')
for d in data:
    print(('\t%d\t%f')%(int(d[0]),d[1]))
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

def mydraw(plot_x,plot_y,xlabel,ylabel):
    pl.plot(plot_x,plot_y,label='roc')
    pl.title('FPR-TPR')
    pl.xlabel=xlabel
    pl.ylabel=ylabel
    pl.legend(loc='upper right')
    pl.show()

   
threshold_list=data[:,1]
plot_x=np.zeros(len(threshold_list))
plot_y=np.zeros(len(threshold_list))
i=0
for threshold in threshold_list:
    plot_x[i],plot_y[i]=calculate_rocxy(data,threshold)#(FPR,TPR)
    #print(plot_data[i])
    i+=1
def AUC(plot_x,plot_y):
    i=0
    s=0
    for dy in plot_y[1:]:
        dx=plot_x[i+1]-plot_x[i]
        i+=1
        s+=dx*dy
    return s
    
mydraw(plot_x,plot_y,'False positive rate','True positive rate')
print(("AUC=%f")%(AUC(plot_x,plot_y)))
