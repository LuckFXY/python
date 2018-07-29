# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:35:06 2017

@author: rain
"""
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from sklearn.metrics import confusion_matrix
DATESZIE=200

#Generate random 3d data sets
import os
print(os.getcwd())
os.chdir("D:\GitHub\python")
c1=np.random.rand(DATESZIE)
c2=np.random.rand(DATESZIE)*(1-c1)
c3=1-c1-c1
tags=np.random.randint(0,3,size=DATESZIE,dtype=int)
data=np.array([tags,c1,c2,(1-c1-c2)]).T
data=data[np.argsort(data[:,-1])[::-1]]
with open("draw_row_test2_data.pickle","wb") as f:
    pickle.dump(data,f)

with open("draw_row_test2_data.pickle","rb") as f:
    data=pickle.load(f)

#print (data)
data=data[np.argsort(data[:,-1])[::-1]]
real_y=data[:,0]
data=data[:,1:]

def printdata(data):
    print('\tLabel\tc0\tc1\tc2')
    for i in range(len(data)):
        print(
                ("\t%d\t%.2f\t%.2f\t%.2f")
                %(int(real_y[i]),data[i][0],data[i][1],data[i][2])
        )


def getpredtags(data,index,TD=0):
    try_data=data.copy()
    try_data[:,index]-=TD
    return np.argmax(try_data,axis=1) 



def calculate_rocxy(data,real_y,index,TD):
    Other=[[1,2],[0,2],[0,1]]
    pred_y=getpredtags(data,index,TD)
    cmatrix=confusion_matrix(real_y,pred_y)  
    
    s=np.sum(cmatrix[:,index])
    if s!=0:
        TPR=cmatrix[index,index] /s
    else:
        TPR=0
    j=Other[index][0]
    s=np.sum(cmatrix[:,j])
    if s!=0:
        FPR1=cmatrix[index,j]/s
    else :
        FPR1=0
    j=Other[index][1]
    s=np.sum(cmatrix[:,j])
    if s!=0:
        FPR2=cmatrix[index,j]/s
    else :
        FPR2=0
    return (FPR1,FPR2,TPR)
'''
def mydraw(plot_x,plot_y,xlabel,ylabel):
    pl.plot(plot_x,plot_y,label='roc')
    pl.title('FPR-TPR')
    pl.xlabel=xlabel
    pl.ylabel=ylabel
    pl.legend(loc='upper right')
    pl.show()
'''
from mpl_toolkits.mplot3d import axes3d
def mydraw(X,Y,Z):
    fig=plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(X, Y, Z)
    
    #ax.plot_wireframe(X,Y,Z,rstride=5,cstride=5)
    #plt.legend()
    plt.show()
   
threshold_list=data[:,-1]
X=np.zeros(len(threshold_list))
Y=np.zeros(len(threshold_list))
Z=np.zeros(len(threshold_list))
i=0
for threshold in threshold_list:
    X[i],Y[i],Z[i]=calculate_rocxy(data,real_y,2,threshold)#(FPR,TPR) index=0
    #print(X[i],Y[i],Z[i])
    i+=1

    
mydraw(X,Y,Z)

