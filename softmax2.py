# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 16:28:45 2016

@author: fxy
"""
 

import os  
import sys  
import time  
  
import numpy  
import pandas as pd
from sklearn import cross_validation

import pylab as pl

import theano  
import theano.tensor as T  

"""
参数说明：
input 输入的一个batch，假设一个batch有n个样本（n_example）
      则input大小就是(n_example,n_in)
n_in  每个样本的大小，MINISt每个样本是一张28*28，n_in=784
n_out 输出的类别书，MNIST 有0~9共10个类别
"""
#=========================================================================
class LogisticRegression(object):
    def __init__(self,input,n_in,n_out):
        #大小是n_in行 n_out列，b为n_out维向量。每一个输出对应W的一列和一个b
        #W 和 b 都定义为theano.shared类型，这样是为了GPU上跑
        self.W = theano.shared(
            value=numpy.zeros(
                (n_in,n_out),
                dtype=theano.config.floatX
            ),
            name='W',
            borrow=True
        )
        self.b = theano.shared(  
            value=numpy.zeros(  
                (n_out,),  
                dtype=theano.config.floatX  
            ),  
            name='b',  
            borrow=True  
        ) 

#input 是(n_example,n_in),W是(n_in,n_out),点乘得到(n_example,n_out),加上b
#n_in=28*28，一个样本，可以看作28*28个属性，每个属性对应10中概率
#在作为T.nnet.softmax的输入，得到p_y_given_x,每一行代表一个样本被估计个类别的概率
#b是n_out维向量，与(n_example,n_out)相加，b与矩阵每一行相加
        
        self.p_y_given_x=T.nnet.softmax(T.dot(input,self.W)+self.b)
#argmax返回最大值下标，因为本例数据集MNIST，下标刚好就是类别。axis=1按行操作
        self.y_pred=T.argmax(self.p_y_given_x,axis=1)
#params,模型的参数
        self.params=[self.W,self.b]
        

#代价函数NLL
#   @ 因为我们是MSGD，每次训练一个batch，一个batch有n_example个样本，
#则y大小是（n_example）
#   @ y.shape[0]样本数，将T.log(self.p_y_given_x)简记为LP
#   @则LP[T.arange(y.shape[0]),y]
#得到[LP[0,y[0]], LP[1,y[1]], LP[2,y[2]], ...,LP[n-1,y[n-1]]] 
#   @最后就平均mean，也就是说，minibatch的SGD，
#是计算出batch里所有样本的NLL平均值，作为cost
#个人：如果正确y[1]对应最大的概率，cost负最大，即最小。妙！

    def negative_log_likelihood(self,y):
        return -T.mean(T.log(self.p_y_given_x)[T.arange(y.shape[0]),y])
            
    def errors(self,y):
        #首先检查y与y_pred的维度是否一样，即是否包含相同的样本数
        if y.ndim!=self.y_pred.ndim:
            raise TypeError(
            'y should have the same shape as self.y_pred',
            ('y',y.type,'y_pred',self.y_pred.type)
            )
        #在检查是不是int类型，是的话计算T.neq(self.y_pred,y)的均值，作误差
        #举个例子，假如self.y_pred=[3,2,3,2,3,2],而实际上y=[3,4,3,4,3,4]  
        #则T.neq(self.y_pred, y)=[0,1,0,1,0,1],1表示不等，0表示相等  
        #故T.mean(T.neq(self.y_pred, y))=T.mean([0,1,0,1,0,1])=0.5，即错误率50%  
        if y.dtype.startswith('int'):
            return T.mean(T.neq(self.y_pred,y)) #妙！
        else:
            return NotImplementedError()
#========================================================================
#loading kaggle dataset
                
def load_data():
    train_csv=pd.read_csv('kaggle\\train.csv')
    train_data=train_csv.values
    
    print '... loading data'
    
    train_set_x,valid_set_x,train_set_y,valid_set_y=\
        cross_validation.train_test_split(\
        train_data[:,1:],train_data[:,0],\
        test_size=0.4,random_state=2016)
#将数据设置成shared variables，主要是为了GPU加速，只有shared variables
#才能存到GPU memory中，只能为float类型，data_y是类别，所以最后又转换成int
    def shared_dataset(data_xy,borrow=True):
        data_x,data_y=data_xy
        shared_x=theano.shared(\
        numpy.asarray(data_x,dtype=theano.config.floatX),borrow=borrow)
        shared_y=theano.shared(\
        numpy.asarray(data_y,dtype=theano.config.floatX),borrow=borrow)
        return shared_x,T.cast(shared_y,'int32')
    
    valid_set_x,valid_set_y=shared_dataset((valid_set_x,valid_set_y))
    train_set_x,train_set_y=shared_dataset((train_set_x,train_set_y))
    
    rval=[(train_set_x,train_set_y),(valid_set_x,valid_set_y)]
    return rval

#========================================================================
#apply model to MNIST dataset rate=0.13
def sgd_optimizaion_mnist(learning_rate=0.05,n_epochs=1000,batch_size=600):
    #load data
    datasets=load_data()
    train_set_x, train_set_y = datasets[0]  
    valid_set_x, valid_set_y = datasets[1]  
    #calculate the number of minibatch,our algorithm is MSGD
    #calculate cost batch by batch
    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size  
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / batch_size  
    
    
    ##########################
    #   building the model   #           
    ##########################
    print '...building the model (0^0)'
    
    #设置变量，index表示minibath的下标 ,x表示训练样本，y是对应的label
    index=T.lscalar()
    x=T.matrix('x')
    y=T.ivector('y')
    
    #定义分类器，用x作为input初始化
    classifier =LogisticRegression(input=x,n_in=28*28,n_out=10)
    
    #定义代价函数，用y来初始化，还有一个隐含的参数x在classifier中
    #cost必须由x和y得来
    cost=classifier.negative_log_likelihood(y)
    

#大神开始讲课了：theano的function函数,givens是字典，其中的x、y是key
#冒号后面是它们的value。fucntion调用时，x，y将被菌体底替换为它们的value
#value里的参数index就是input=[index]
#Eg: test_model(1)
#首先根据index=1具体化x为test_set_x[1*batch_size:(1+1)*batch_size]
#具体化y为test_set_y[1*batch_size:(1+1)*batch_size]
#然后计算output=classifier.errors(y)
#个人：切片即使超出范围会返回边界 eg: x=[1] x[0:1]=x[0:10]=[1]


    validate_model=theano.function(
        inputs=[index],
        outputs=classifier.errors(y),
        givens={
            x:valid_set_x[index*batch_size:(index+1)*batch_size],
            y:valid_set_y[index*batch_size:(index+1)*batch_size]
        }
    )
    
#计算各个参数的梯度,cost是个函数，wrt是变量集合
    g_W=T.grad(cost=cost,wrt=classifier.W)
    g_b=T.grad(cost=cost,wrt=classifier.b)    

#更新的规则，根据梯度下降法的更新公式
    updates=[(classifier.W,classifier.W-learning_rate*g_W),
             (classifier.b,classifier.b-learning_rate*g_b)]
             
#train_model 比test_model多了一个update
    train_model=theano.function(
        inputs=[index],
        #outputs=cost,
        outputs=classifier.errors(y),
        updates=updates,
        givens={
            x:train_set_x[index*batch_size:(index+1)*batch_size],
            y:train_set_y[index*batch_size:(index+1)*batch_size]
        }
    )
#######################
#    start to train   #
#######################
    print '...training the model  !<*v*>!'
    
    patience=5000
    patience_increase=2
#提高的阈值，在验证误差减小到之前的0.995倍是，会更新best_validaion_loss
    improvement_threshold=0.995
#这样设置validation_frequency可以保证每一次epoch都会在验证集上测试？？？
    validation_frequency=min(n_train_batches,patience/2)
    
    #最好的验证集上的loss，最好的即最小。初始化为无穷大
    best_validation_loss=numpy.inf
    this_validation_loss=numpy.inf #初始化
    this_error=1.1
    min_error=1.   
    
    start_time=time.clock()
    
    done_looping=False
    epoch=0
    

#大神又开始讲课了： 下面就是训练过程了 
#    while循环控制时，步数epoch,一个epoch会便利所欲的batch，即所欲的图片？
#    for循环遍历一个batch,一次一个。内用train_model(minibatch_index)去训练模型
#    train_model里的update会更新各个参数。
#    for循环里面会累加训练过的batch数iter,当iter是validation_frequency倍数时
#则会在验证集上测试，如果验证集的损失this_validation_loss小于之前最佳的损失
#best_validation_loss,则更新best_validation_loss和best_iter，同时在testset
#上测试
#    如果验证集的损失this_validation_loss 小于
#best_validation_loss*improvement_threshold时则更新patience.
#    当达到最大步数n_epoch时，或者patience<iter时，训练结束
#个人注解：
#    xrange 比range高效一点，但是返回对象，不是list
#    n_epochs=1000
#    print('num:%d %%' % (123)) %是 转义符号
#    validation_frequency=n_train_batches=10(计算出来的)
    
    rd_epoch=numpy.ones(100)
    rd_iter=numpy.ones(100,dtype='int')
    rd_error=numpy.ones(100)    
    rd_error2=numpy.ones(100)  
    rd_index=0
    while(epoch<n_epochs) and (not done_looping):
        epoch=epoch+1
        for minibatch_index in xrange(n_train_batches):
            
            this_error=train_model(minibatch_index)
            #iteration number ? 是为了统计总迭代次数
            iter=(epoch-1)*n_train_batches+minibatch_index
            #每进行一个batch就验证一次
           # if(iter+1) % validation_frequency ==0 :

            if min_error >this_error:
                rd_iter[rd_index]=iter
                rd_epoch[rd_index]=epoch+( minibatch_index + 1)/n_train_batches*1.0
                rd_error[rd_index]=this_error
                rd_index+=1
                min_error=this_error
                #imporve patience if loss improvement is good enough
                if this_validation_loss < best_validation_loss\
                    *improvement_threshold:
                    patience=max(patience,iter*patience_increase)
                    best_validation_loss=this_validation_loss
                #test it on the validation set
                
                validation_losses=[validate_model(i)\
                                   for i in xrange(n_valid_batches)]
                this_validation_loss=numpy.mean(validation_losses)
                rd_error2[rd_index]=this_validation_loss
                print(  
                    'epoch %i, minibatch %i/%i, validation error %f %%' %  
                    (  
                        epoch,  
                        minibatch_index + 1,  
                        n_train_batches,  
                        this_validation_loss * 100.  
                    )  
                )  
        if patience <=iter:
            done_looping =True
            break
 #while循环结束       
    end_time=time.clock()     
                                
    print(  
        (  
        'Optimization complete with best validation score of %f %%,'    
        )  
        % (best_validation_loss * 100.)  
    )  
    print 'The code run for %d epochs, with %f epochs/sec' % (  
        epoch, 1. * epoch / (end_time - start_time))  
    
    print >> sys.stderr, ('The code for file ' +  
        os.path.split(__file__)[1] +  
        ' ran for %.1fs' % ((end_time - start_time)))                                 
                                           
    
    pl.plot(rd_epoch,rd_error,label='train')
    pl.plot(rd_epoch,rd_error2,label='valid')
    
    pl.title('epoch-error')
    pl.xlabel('epoch')
    pl.ylabel('error')
    pl.legend(loc='upper right')
    pl.xlim(0,15)
    pl.ylim(0,0.8)
    pl.show()
    
    rd_iter=rd_iter[:rd_index]
    rd_error=rd_error[:rd_index]
    rd_error2=rd_error2[:rd_index]
    pl.plot(rd_iter,rd_error,label='train')
    pl.plot(rd_iter,rd_error2,label='valid')
    
    pl.title('iter-error')
    pl.xlabel('iter')
    pl.ylabel('error')
    pl.legend(loc='upper right')
    pl.xlim(0,100)
    pl.ylim(0,0.8)
    pl.show()
if __name__=='__main__':
    sgd_optimizaion_mnist()
