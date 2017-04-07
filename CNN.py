# -*- coding: utf-8 -*-
"""
Created on Sun May 15 16:34:00 2016

@author: Administrator
"""

import cPickle
import gzip
import os
import sys
import time

import numpy 

import theano
import theano.tensor as T
from theano.tensor.signal import downsample
from theano.tensor.nnet import conv

'''
大神说话了
卷积+下采样合成一个LeNetConvPoolLayer
rng:随机数生成器，用于初始化W
input:4维的向量，theano.tensor.dtensor4
filter_shape:(number of filters,num input feature maps,filter height,filter width)
image_shape(batch size,num input feature maps,image height,image width)
poolsize:(#row,#cols)
'''
#==================Convoluation & pooling layer====================================
class LeNetConvPoolLayer(object):
    def __init__(self,rng,input,filter_shape,image_shape,poolsize=(2,2),W=None,b=None):
        #image_shape[1]和filter_shape[1]都是num input feature maps它们必须一样
        assert image_shape[1]==filter_shape[1] #输入特征图的个数
        self.input=input
        
        #每个隐层神经元（像素）与上一层的连接数为（卷积输入）
        #prod返回各元素的乘积
        fan_in=numpy.prod(filter_shape[1:])
        
        #lower layer上每个神经元获得的梯度来自（卷积输出）
        #num output feature maps* filter height * filter width/pooling size
        fan_out=(filter_shape[0]*numpy.prod(filter_shape[2:])/
                numpy.prod(poolsize))
        #以上求得fan_in,fan_out,将他们呢带入公式，从此来随机初始化W，W就是线性卷积核
    
        W_bound=numpy.sqrt(6./(fan_in+fan_out))
        if W is None:
            W=numpy.asarray(
                rng.uniform(low=-W_bound,high=W_bound,size=filter_shape),
                dtype=theano.config.floatX
            )
        self.W=theano.shared(value=W,borrow=True)
        
        #偏置是一维向量，每一个特征图对应一个偏置
        #输出的特征图的个数由filter个数决定，因此用filter_shape[0]即number of filters初始化
        if b is None:
            b=numpy.zeros((filter_shape[0],),dtype=theano.config.floatX)
        self.b=theano.shared(value=b,borrow=True)
        
        #将输入图像与filter卷积，conv.conv2d
        #卷积完没有加b再通过sigmoid,这里简化了
        conv_out=conv.conv2d(
            input=input,
            filters=self.W,
            filter_shape=filter_shape,
            image_shape=image_shape
        )
        
        #maxpooling,最大子采样过程
        pooled_out=downsample.max_pool_2d(
            input=conv_out,
            ds=poolsize,
            ignore_border=True
        )
        
        #加偏置，再通过tanh映射，得到卷积+子采样层的最终输出
        #因为b是一位向量，这里用维度转化函数dimshuffle将其reshape.比如b是（10,),
        #则b.dimshuffle('x',0,'x','x')将其变为(1,10,1,1)
        self.output=T.tanh(pooled_out+self.b.dimshuffle('x',0,'x','x'))
        #卷积+采样层的参数
        self.params=[self.W,self.b]
 


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
            W = numpy.asarray(
                rng.uniform(
                    low=-numpy.sqrt(6./(n_in+n_out)),
                    high=numpy.sqrt(6./(n_in+n_out)),
                    size=(n_in,n_out)
                ),
                dtype=theano.config.floatX
            )
        if activation==theano.tensor.nnet.sigmoid:
            W*=4
                
        W=theano.shared(value=W,name='W',borrow=True)
            
        if b is None:
            b=numpy.zeros((n_out,),dtype=theano.config.floatX)
            
        b=theano.shared(value=b,name='b',borrow=True)
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
    def __init__(self,input,n_in,n_out,W,b):
        #大小是n_in行 n_out列，b为n_out维向量。每一个输出对应W的一列和一个b
        #W 和 b 都定义为theano.shared类型，这样是为了GPU上跑
        if W is None:
            W=numpy.zeros(
                (n_in,n_out),
                dtype=theano.config.floatX
            )
        self.W = theano.shared(value=W,name='W',borrow=True)
        
        if b is None:
            b=numpy.zeros(  
                (n_out,),  
                dtype=theano.config.floatX  
            )
        self.b = theano.shared(value=b,  name='b',  borrow=True ) 
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
#=======================loading MNIST dataset=======================
                
def report_hook(count,block_size,total_size):
    c=block_size/1024/1024
    t=total_size/1024/1024
    print '%f / %f %02d'%(c,t,100*c/t)
def load_data(dataset):
    #dataset是数据集的路径，程序首 先检测该路径下有没有minst数据集，没有的话就下载
    data_dir,data_file=os.path.split(dataset)
    if data_dir == "" and not os.path.isfile(dataset):
        #check if dataset is in the data directory
        new_path=os.path.split(__file__)[0]+'/'+dataset  
        if os.path.isfile(new_path) or data_file == 'mnist.pkl.gz':
            dataset=new_path
        
    if(not os.path.isfile(dataset)) and data_file == 'mnist.pkl.gz':
        import urllib
        origin =(
            'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz' 
        )
        print 'Downloading data from %s' %origin
        print 'To ',dataset
    #    write=open(dataset,'wb')
    #    write.close
        urllib.urlretrieve(origin,dataset,reporthook=report_hook)
    print '... loading data'
#以上是检测并下载数据集mnist.pkl.gz，不是本文重点。下面才是load_data的开始  
      
#从"mnist.pkl.gz"里加载train_set, valid_set, test_set，它们都是包括label的  
#主要用到python里的gzip.open()函数,以及 cPickle.load()。  
#‘rb’表示以二进制可读的方式打开文件  
    f = gzip.open(dataset, 'rb')  
    train_set, valid_set, test_set = cPickle.load(f)  
    f.close()
#将数据设置成shared variables，主要是为了GPU加速，只有shared variables
#才能存到GPU memory中，只能为float类型，data_y是类别，所以最后又转换成int
    def shared_dataset(data_xy,borrow=True):
        data_x,data_y=data_xy
        shared_x=theano.shared(\
        numpy.asarray(data_x,dtype=theano.config.floatX),borrow=borrow)
        shared_y=theano.shared(\
        numpy.asarray(data_y,dtype=theano.config.floatX),borrow=borrow)
        return shared_x,T.cast(shared_y,'int32')
    
    test_set_x,test_set_y=shared_dataset(test_set)
    valid_set_x,valid_set_y=shared_dataset(valid_set)
    train_set_x,train_set_y=shared_dataset(train_set)

    read_file=open('kaggle\\params.py','rb')
    try:
        params=cPickle.load(read_file)
        print 'loaded params!'
    finally:
        read_file.close()   
       
    rval=[(train_set_x,train_set_y),(valid_set_x,valid_set_y),\
          (test_set_x,test_set_y),params]
          
    return rval            
#===========================LeNet-5 demo================================
def evaluate_lenet5(learning_rate=0.1,n_epochs=1,
                    dataset='mnist.pkl.gz',
                    nkerns=[20,50],batch_size=500):
    '''
    n_epochs训练步数，每一次都会遍历所有batch，即所有样本
    batch_size这里设置500,每遍历500个样本，才计算梯度
    nkerns=[20,50],每一个LeNetConvPoolLayer卷积核的个数，第一层20个核，第二层50
    '''
    
    rng=numpy.random.RandomState(2016)
    
    #加载数据
    datasets=load_data(dataset)
    train_set_x, train_set_y = datasets[0]  
    valid_set_x, valid_set_y = datasets[1]  
    test_set_x, test_set_y = datasets[2]  
    params=datasets[3]
    #就算batch的个数
    n_train_batches = train_set_x.get_value(borrow=True).shape[0]  
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0]  
    n_test_batches = test_set_x.get_value(borrow=True).shape[0]  
    n_train_batches /= batch_size  
    n_valid_batches /= batch_size  
    n_test_batches /= batch_size  
    
    #定义几个变量，index表示batch下标，x编制输入的训练数据，y是对应的标签
    index=T.lscalar()
    x=T.matrix('x')
    y=T.ivector('y')
    
    ######################
    # BUILD ACTUAL MODEL #
    ######################
    print '...building the model'
    #我们加载数据是(batch_size,28*28),但是LeNetConvPoolLayer输入是四维的
    layer0_input=x.reshape((batch_size,1,28,28))
    '''
    layer0即第一个LeNetConvPoolLayer层
    输入的单张图片(28,28)经过conv得到（28-5+1，28-5+1）=（24，24）
    经过maxpooling得到（24/2，24/2）=（12，12）
    因为每一个batch都有batch_size张图，第一个LeNetConvPoolLayer层有nkerns[0]卷积核
    故layer0输出为（batch_size,nkerns[0],12,12)
    '''
    layer0=LeNetConvPoolLayer(        
        input=layer0_input,
        rng=rng,
        image_shape=(batch_size,1,28,28),
        filter_shape=(nkerns[0],1,5,5),
        poolsize=(2,2),
        W=params[6],
        b=params[7]
    )
    '''
    layer1即第二层
    输入时layer0的输出，每张特征图为(12,12),经过conv得到（12-5+1，12-5+1）=（8，8）
    经过maxpooling得到(8/2,8/2)=(4,4)
    因为每个batch有batch_size，第二层有nkerns[1]个卷积核
    故layer1输出为(batch_size,nkerns[1],4,4)
    '''
    layer1=LeNetConvPoolLayer(
        rng,
        input=layer0.output,
        #输入nkerns[0]张特征图，即layer0输出
        image_shape=(batch_size,nkerns[0],12,12),
        filter_shape=(nkerns[1],nkerns[0],5,5),
        poolsize=(2,2),
        W=params[4],
        b=params[5]
        
    )
    '''
    定义好前二层layer0,layer1的卷积层，然后开始定义全连接层layer2
    用HiddenLayer老初始化layer2,layer2输入二维(batch_size,num_pixels)
    故要将将上一层通过以图像全部（卷积层输出）特征图合并为一维向量
    将layer1的输出(batch_size,nerkns[1],4,4)flatten为
    (batch_size,nkerns[1]*4*4)=(500,800)
    表示500个样本，每一行代表一个样本。layer2输出大小(batch_size,n_out)=(500.500)
    '''
    layer2_input=layer1.output.flatten(2)
    layer2= HiddenLayer(
        input=layer2_input,
        rng=rng,
        n_in=nkerns[1]*4*4,
        n_out=500,
        activation=T.tanh,
        W=params[2],
        b=params[3]
    )
    '''
    最后一层就ishi分类器层
    输入(500,500),输出(500,10)
    '''
    
    layer3=LogisticRegression(
        input=layer2.output,
        n_in=500,
        n_out=10,
        W=params[0],
        b=params[1]
        )
    
    #代价函数NLL
    cost=layer3.negative_log_likelihood(y)
    
    '''
    test_model计算测试无法,x,y格局给定的index 具体化，调用layer3,
    layer3又会逐层的调用layer2,layer1,layer0,故test_model其实就是整个CNN结构
    test_model的输入时x,y输出是layer3.error(y)的输出，即误差
    '''
    test_model=theano.function(
        inputs=[index],
        outputs=layer3.errors(y),
        givens={  
            x: test_set_x[index * batch_size: (index + 1) * batch_size],  
            y: test_set_y[index * batch_size: (index + 1) * batch_size]  
        } 
    )
    #validate_model，验证模型，分析同上。  
    validate_model = theano.function(  
        [index],  
        layer3.errors(y),  
        givens={  
            x: valid_set_x[index * batch_size: (index + 1) * batch_size],  
            y: valid_set_y[index * batch_size: (index + 1) * batch_size]  
        }  
    ) 

    #下面是train_model，优化设计到SGD,需要计算梯度，更新参数
    #参数集合
    params=layer3.params+layer2.params+layer1.params+layer0.params
    
    ret_model_params=theano.function(
        inputs=[],
        outputs=params
    )    

    #对各个参数的梯度
    grads=T.grad(cost,params)
    #由于参数太多，在update里写很麻烦，所有用for in 
    updates=[
        (param_i,param_i-learning_rate*grad_i)
        for param_i,grad_i in zip(params,grads)
    ]
    
    #train_model，代码分析同test_model。train_model里比test_model、validation_model多出updates规则  
    train_model = theano.function(  
        inputs=[index],  
        outputs=cost,  
        updates=updates,  
        givens={  
            x: train_set_x[index * batch_size: (index + 1) * batch_size],  
            y: train_set_y[index * batch_size: (index + 1) * batch_size]  
        }  
    )  
    
    ################
    #   开始训练   #
    ################
    print '...training'
    patience = 10000    
    patience_increase = 2    
    improvement_threshold = 0.995   
                                     
    validation_frequency = min(n_train_batches, patience / 2)  
 #这样设置validation_frequency可以保证每一次epoch都会在验证集上测试。  
  
    best_validation_loss = numpy.inf   #最好的验证集上的loss，最好即最小  
    this_validation_loss=numpy.inf
    best_iter = 0                      #最好的迭代次数，以batch为单位。比如best_iter=10000，说明在训练完第10000个batch时，达到best_validation_loss  
    test_score = 0.  
    start_time = time.clock()  
  
    epoch = 0  
    done_looping = False  
    
    #大神说了
    #下面就是训练过程了，while循环控制的时步数epoch，一个epoch会遍历所有的batch，即所有的图片。  
    #for循环是遍历一个个batch，一次一个batch地训练。for循环体里会用train_model(minibatch_index)去训练模型，  
    #train_model里面的updatas会更新各个参数。  
    #for循环里面会累加训练过的batch数iter，当iter是validation_frequency倍数时则会在验证集上测试，  
    #如果验证集的损失this_validation_loss小于之前最佳的损失best_validation_loss，  
    #则更新best_validation_loss和best_iter，同时在testset上测试。  
    #如果验证集的损失this_validation_loss小于
    #best_validation_loss*improvement_threshold时则更新patience。  
    #当达到最大步数n_epoch时，或者patience<iter时，结束训练  
    while(epoch<n_epochs) and (not done_looping):
        epoch=epoch+1
        for minibatch_index in xrange(n_train_batches):
            iter=(epoch-1)*n_train_batches+minibatch_index
            if iter %100 == 0:
                print 'training @ iter =',iter
            cost_ij=train_model(minibatch_index)#!!!
            if (iter+1)%validation_frequency==0:
                validation_losses=[validate_model(i) for i
                                    in xrange(n_valid_batches)]
                this_validation_loss=numpy.mean(validation_losses)
                print (
                    'epoch %i,minibatch %i/%i,validation error %f %%'%
                    (epoch,minibatch_index+1,n_train_batches,
                     this_validation_loss*100.)
                )
                
                if this_validation_loss < best_validation_loss:
                    
                    if this_validation_loss < best_validation_loss \
                        * improvement_threshold :                     
                        patience=max(patience,iter*patience_increase)
                        
                    best_validation_loss=this_validation_loss
                    #best_iter=iter
                    
                    test_losses=[test_model(i) for i
                                in xrange(n_test_batches)
                    ]
                    test_score=numpy.mean(test_losses)
                    print(
                    'good job! test error of best model %f %% iter=%i'%
                    (test_score*100.,iter)
                    )
            if patience<=iter:
                done_looping = True
                break
    end_time=time.clock()
    print ('Optimization complete')
    print (
        'Best validation score of %f %% with test performance %f %%'%
        (best_validation_loss*100.,test_score*100.)
    )
    print >> sys.stderr,('The code of file'+
                         os.path.split(__file__)[1]+
                         'ran for %.2fm' %((end_time-start_time)/60.)
            )
    print 'saving....'
    params=ret_model_params()
    write_file = open('kaggle\\params.py', 'wb')    
    cPickle.dump(params, write_file, -1)    
  
    write_file.close()  
    print 'finished!'
    
if __name__=='__main__':
    evaluate_lenet5()
