# -*- coding: utf-8 -*-
"""
Created on Fri May 06 14:50:00 2016

@author: Administrator
"""

import os
import sys
import time

import pandas as pd
import pylab as pl
from sklearn import cross_validation

import numpy

import theano
import theano.tensor as T
#=======================loading kaggle dataset=======================
                
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

#=============================HiddenLayer============================

class HiddenLayer(object):
    def __init__(self,input,rng,n_in,n_out,W=None,b=None,\
    activation=T.tanh):
#函数参数
#input     :输出即隐藏层的神经元个数。输入层与隐层全连接一共n_in*n_out个权重
#           故w大小时（n_in,n_out)每一列对应隐层的每个神经元的连接权重
#           大小（n_example,n_in）一行一个样本，每一行MLP的输入层
#b         :偏置，隐层有n_out个神经元，b是n_out维向量
#rng       :随机数生成器，numpy.random.RandomState,用于初始化W
#activation:激活函数，这里定义为tanh
        self.input=input #类HiddenLayer的input即所传递进来的input

#参数初始化
#数据定义 ：GPU必用theano.config.floatX & theano.shared
#W初始规则：tanh 在正负sqrt(6./(n_in+h_hidden))之间
#          sigmoid 范围*4
#有时可以用以前训练好的参数来初始化
        if W is None:
            W_values = numpy.asarray(
                rng.uniform(
                    low=-numpy.sqrt(6./(n_in+n_out)),
                    high=numpy.sqrt(6./(n_in+n_out)),
                    size=(n_in,n_out)
                ),
                dtype=theano.config.floatX
            )
            if activation==theano.tensor.nnet.sigmoid:
                W_values*=4
            W=theano.shared(value=W_values,name='W',borrow=True)
            
        if b is None:
            b_values=numpy.zeros((n_out,),dtype=theano.config.floatX)
            b=theano.shared(value=b_values,name='b',borrow=True)
#隐层内W，b 
        self.W=W
        self.b=b
#隐层的输出
        lin_output=T.dot(input,self.W)+self.b
        self.output=(
            lin_output if activation is None else activation(lin_output)
        )
#隐层的参数
        self.params=[self.W,self.b]
        
#===========================LogisticRegression=========================

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
#n_in=28*28，一个样本，可以看作28*28个属性，每个属性对应n_out概率
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
           
#===================================MLP===============================
class MLP(object):
    def __init__(self, input, rng, n_in, n_hidden, n_out):
        self.hiddenLayer=HiddenLayer(
            input=input,
            rng=rng,
            n_in=n_in,
            n_out=n_hidden,
            activation=T.tanh
        )
#将隐藏层hiddenLayer的输出作为分类层LogRegressionLayer的输入,连接
        self.logRegressionLayer=LogisticRegression(
            input=self.hiddenLayer.output,
            n_in=n_hidden,
            n_out=n_out
        )

#MLP模型的其他参数

#规则化项：常见的L1、L2_sqr
        self.L1=(
            abs(self.hiddenLayer.W).sum()+
            abs(self.logRegressionLayer.W).sum()
        )        
        
        self.L2_sqr=(
            (self.hiddenLayer.W **2).sum()+
            (self.logRegressionLayer.W**2).sum()
        )
#损失函数NLL        
        self.negative_log_likelihood=(
            self.logRegressionLayer.negative_log_likelihood
        )
#误差
        self.errors=self.logRegressionLayer.errors
#MLP的参数
        self.params=self.hiddenLayer.params+self.logRegressionLayer.params        
        #end-snippet-3
        
#===============================building models=================      
#test_mlp 是一个应用实例，用梯度下降法优化MLP,针对MNIST数据集
def test_mlp(learning_rate=0.003,L1_reg=0.001,L2_reg=0.01,n_epochs=20,
             batch_size=20,n_hidden=500):
#learning_rate
#L1_reg,L2_reg：正则化项钱的系数，权衡正则化项羽NLL项的比重
#代价函数      ：NLL+L1*reg*L1+L2_reg*L2_sqr
#n_epochs     :迭代最大次数，程序最大运行次数
#dataset      :训练集路径
#n_hidden     ：隐藏层神经元个数
#batch_size=20:没训练完20个样本才计算梯度并更新参数
    datasets=load_data() 
    train_set_x, train_set_y = datasets[0]  
    valid_set_x, valid_set_y = datasets[1]  

#shape[0]获得行数，一行代表一个样本，故获取的是样本数，
#除以batch_size可以得到有多少个batch  
    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size  
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / batch_size  
 
########################
# BUILD ACTUAL MODEL   #
########################
    print '... building the model'
    
#index 表示batch的下标，标量
#x     表示数据集
#y      表示类别，一维向量
    index =T.lscalar()
    x=T.matrix('x')
    y=T.ivector('y')
    
    rng=numpy.random.RandomState(2016)
    
#生成一个MLP，命名为classifier
    classifier =MLP(
        input=x,
        rng=rng,       
        n_in=28*28,
        n_hidden=n_hidden,
        n_out=10
    )
    
#代价函数，有规则化项
#用y来初始化，而其实还有一个隐含的参数x在classifier
    cost=(
        classifier.negative_log_likelihood(y)
        +L1_reg * classifier.L1
        +L2_reg * classifier.L2_sqr
    )
    
#theano的function函数
#这里有参数y和隐含x，所有gibens里面具体化的x,y传递进去
    
    ret_model_params=theano.function(
        inputs=[],
        outputs=classifier.params
    )
    
    validate_model = theano.function(  
        inputs=[index],  
        outputs=classifier.errors(y),  
        givens={  
            x: valid_set_x[index * batch_size:(index + 1) * batch_size],  
            y: valid_set_y[index * batch_size:(index + 1) * batch_size]  
        }  
    )  
    
#cost函数对各个参数的偏导数值，即梯度，存在gparams
    gparams=[T.grad(cost,param) for param in classifier.params]
    
#参数更新规则
#updates[(),(),()....],每个括号的内容都是(param,param-learning_rate*gpraram)
    updates=[
        (param,param-learning_rate * gparam)
        for param,gparam in zip(classifier.params,gparams)
    ]
    
    train_model=theano.function(
        inputs=[index],
        outputs=(cost,classifier.errors(y)),
        updates=updates,
        givens={
            x: train_set_x[index*batch_size: (index + 1)*batch_size],
            y: train_set_y[index*batch_size: (index + 1)*batch_size]         
        }
    )
    
    ###################
    #  start to train #
    ###################
    print '...training'
    
    patience=10000
    patience_increase=2
    
#提高的阈值，在验证误差减小到之前的0.995倍时，会更新best_validation_loss    
    improvement_threshold = 0.995    
#这样设置validation_frequency可以保证每一次epoch都会在验证集上测试。 patience？？？   
    validation_frequency = min(n_train_batches, patience / 2)  
    
    best_validation_loss=numpy.inf
    this_validation_loss=numpy.inf

    this_cost=numpy.inf
    min_cost=numpy.inf     
    
    start_time=time.clock()
    
#epoch即训练部署，每个epoch都会遍历所有训练数据
    epoch=0
    done_looping=False

    
#终于开始训练了，while循环控制的步数epoch，一个epoch会遍历所有的batch，即素有的图片。
#for循环遍历一个个batch，一次一个batch训练，for内用train_model(minibatch_index)去训练
#train——model的updatas会更新各个参数
#for循环里面会离家训啦过的batch数iter，iter是validation_frequency倍数时验证集测试
#如果验证集的损失this_validation_loss小于之前最佳的损失best_valiation_loss,
#    则更新best_validation_loss和best_iter,同时在testset上测试
#如果验证集合的损失this_validation_loss 小于best_validation_loss*improvement_threshold
#   则更新patience
#当达到最大步数n_epoch时，或者patience<iter结束
    
    rd_epoch=numpy.ones(1000)
    rd_iter=numpy.ones(1000,dtype='int')
    rd_error=numpy.ones(1000)    
    rd_error2=numpy.ones(1000)  
    rd_index=0   
    
    while(epoch <n_epochs) and (not done_looping):
        epoch=epoch+1
        for minibatch_index in xrange(n_train_batches):
            
            this_cost,this_error=train_model(minibatch_index)#!!!!!
            
            #已经训练过的minibatch数，即贴袋次数iter
            iter=(epoch-1) * n_train_batches+minibatch_index
            
            if min_cost*0.85 > this_cost:
                min_cost=this_cost
                rd_iter[rd_index]=iter
                rd_epoch[rd_index]=epoch+( minibatch_index + 1)/n_train_batches*1.0
                rd_error[rd_index]=this_error
                rd_index+=1
                #当前验证误差比之前的都小，则更新best_validaiton_loss，以及best_iter
                #并且在valid_data上进行测试
                                    
                validation_losses=[validate_model(i) 
                                    for i in xrange(n_valid_batches)]#!!!!!
                this_validation_loss=numpy.mean(validation_losses)
                
                if this_validation_loss < best_validation_loss:
                    if(
                        this_validation_loss < best_validation_loss*
                        improvement_threshold
                    ):
                        patience=max(patience,iter*patience_increase)
                    best_validation_loss=this_validation_loss
                
                
                rd_error2[rd_index]=this_validation_loss   
                print(  
                    ('epoch %i, minibatch %i/%i, train cost %f,train error %f %%')%  
                    (  
                        epoch,  
                        minibatch_index + 1,  
                        n_train_batches,  
                        this_cost,                    
                        this_error * 100.  
                    )  
                ) 
                print ('validation error %f %%')% (this_validation_loss*100.)
            if patience<iter:
                done_looping=True
                break
    end_time=time.clock()
    print(  
        'epoch %i, minibatch %i/%i, validation error %f %%' %  
            (  
            epoch,  
            minibatch_index + 1,  
            n_train_batches,  
            this_validation_loss * 100.  
            )  
         )
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
    '''                                    
    pl.plot(rd_epoch,rd_error,label='train')
    pl.plot(rd_epoch,rd_error2,label='valid')
    
    pl.title('epoch-error')
    pl.xlabel('epoch')
    pl.ylabel('error')
    pl.legend(loc='upper right')
    pl.xlim(0,15)
    pl.ylim(0,0.8)
    pl.show()
    '''
    rd_iter=rd_iter[:rd_index]
    rd_error=rd_error[:rd_index]
    rd_error2=rd_error2[:rd_index]
    pl.plot(rd_iter,rd_error,label='train')
    pl.plot(rd_iter,rd_error2,label='valid')
    
    pl.title('iter-error')
    pl.xlabel('iter')
    pl.ylabel('error')
    pl.legend(loc='upper right')
    #pl.xlim(0,100)
    #pl.ylim(0,0.8)
    pl.show()
    
if __name__=='__main__':
    test_mlp()
