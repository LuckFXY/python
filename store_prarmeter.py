# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#you can save your parameter as follow
import cPickle
a=[1,2,3]
b={4:5,6:7}
write_file=open('test','wb')
cPickle.dump(a,write_file,-1)
cPickle.dump(b,write_file,-1)
write_file.close();

read_file=open('test','rb')
a_1=cPickle.load(read_file)
b_1=cPickle.load(read_file)
print a_1,b_1
read_file.close()
#if the definition of w,b is shared
#use following codes
#保存  
write_file = open('path', 'wb')    
cPickle.dump(w.get_value(borrow=True), write_file, -1)    
cPickle.dump(v.get_value(borrow=True), write_file, -1)    
cPickle.dump(u.get_value(borrow=True), write_file, -1)   
write_file.close()  
  
#读取  
read_file = open('path')  
w.set_value(cPickle.load(read_file), borrow=True)  
v.set_value(cPickle.load(read_file), borrow=True)  
u.set_value(cPickle.load(read_file), borrow=True)  
read_file.close()  
#you can package the codes into a function 
def save_params(param1,param2):  
    import cPickle  
    write_file = open('params', 'wb')   
    cPickle.dump(param1.get_value(borrow=True), write_file, -1)  
    cPickle.dump(param2.get_value(borrow=True), write_file, -1)  
    write_file.close()  
    
#read your prarmeter
if os.path.exists('params'):  
        f=open('params')  
        self.W.set_value(cPickle.load(f), borrow=True)  
        self.b.set_value(cPickle.load(f), borrow=True) 