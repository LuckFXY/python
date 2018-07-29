# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 17:29:15 2016

@author: fxy
"""

import numpy as np
from pylab import scatter, show, legend, xlabel, ylabel,plot
from math import e
#load the dataset
data=np.loadtxt('ml_data/data1.txt',delimiter=',')
X = data[:, 0:2]  
y = data[:, 2]  
y.shape=(100,1)
'''  
pos = np.where(y == 1)  
neg = np.where(y == 0)  
scatter(X[pos, 0], X[pos, 1], marker='o', c='b')  
scatter(X[neg, 0], X[neg, 1], marker='x', c='r')  
xlabel('Feature1/Exam 1 score')  
ylabel('Feature2/Exam 2 score')  
legend(['Fail', 'Pass'])  
show()  
'''

def sigmoid(x):
    #compute sigmoid fucntion
    den=1.0+ e **(-1.0*x)
    gz=1.0/den
    return gz
    
def compute_cost(theta,x,y):
    #computes cost given prediected and actual value  
    m=x.shape[0] #number of training example
    theta=np.reshape(theta,(len(theta),1))
    z=x.dot(theta)
    print z[np.where(z<1)].size
    j=(1./m)*(\
    -np.transpose(y).dot(np.log(sigmoid(z)))\
    -np.transpose(1-y).dot(np.log(1-sigmoid(z)))
    )
    #grad=transpose((1./m)*transpose(sigmoid(x.dot(theta))-y).dot(x))
    #optimize.fmin expects a single value,so cannot return grad
    return j
    
def compute_grad(theta,x,y):
    theta.shape=(1,3)
    grad=np.zeros(3)
    h=sigmoid(x.dot(theta.T))
    delta = h-y
    l=grad.size
    m=x.shape[1]
    for i in range(l):
        sumdelta=delta.T.dot(x[:,i])
        grad[i]=(1.0/m)*sumdelta
    theta.shape=(3,)
    return grad

def judge(theta,x,y):
    h=sigmoid(x.dot(theta.T))
    o=np.zeros(len(y))
    o[h>0.5]=1
    o.shape=(len(y),1)
    s=o[np.where(o==y)].size *1.0 /len(y)
    return s
    
    
def training(X,y,a=0.005):
  #  theta=np.random.randn(3)
    theta=np.array([0,0,0])
    e=np.eye(2,3)
    e[1,2]=0
    x=X.dot(e)
    x[:,2]=1
    j=-1.0
    time=0
    best_j=0.0
    best_theta=0
    while((abs(best_j-j)>0.005) or (best_j<0.93)):
        theta=theta-a*compute_grad(theta,x,y)
        j=judge(theta,x,y)
        if(j>best_j):
            best_j=j
            best_theta=theta
 #           print time,'\t',theta,'\t',j
            print '.',
        time+=1
        
    print '\nfinished result:',best_theta,' ',best_j
    return best_theta,time
    
if __name__ == '__main__':
    #test
    bt=[  -4.36840312, 5.17493772 ]  
#    bt,time=training(X,y)
    pos = np.where(y == 1)  
    neg = np.where(y == 0)  
    scatter(X[pos, 0], X[pos, 1], marker='o', c='b')  
    scatter(X[neg, 0], X[neg, 1], marker='x', c='r')  
    xlabel('Feature1/Exam 1 score')  
    ylabel('Feature2/Exam 2 score')  
    legend(['Fail', 'Pass']) 
    x1=[0,bt[0]]
    y1=[0,bt[1]]
    plot(x1,y1)    
    show(x1,y1)  


def predict(theta,x):
    #predict label using learned logistic regression parameters
    m,n=x.shape
    p=np.zeros(shape=(m,1))
    h=sigmoid(x.dot(theta.T))
    for it in range(0,h.shape[0]):
        if h[it]>0.5 :
            p[it,0]=1
        else :
            p[it,0]=0
    return p
#compute_cost(theta,X,y)    
#p=predict(np.array(theta),it)
#print 'Train Accuract: %f'%(y[np.where(p==y)].size/float(y.size)*100)