# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 22:49:57 2017

@author: rain
"""

class  Test:  
    """ 
    Class test 
    """  
    EventMethods_Test1 = "func1"  
    EventMethods_Test2 = 2  
    EventMethods_Test3 = 3  
  
    def __init__( self ):  
        self.initEventMethods()  
        self.EventMethods["func1"]()  
  
    def initEventMethods(self):  
        self.EventMethods = {  
                Test.EventMethods_Test1: self.EventMethods_Func1,  
                Test.EventMethods_Test2: self.EventMethods_Func2,  
                Test.EventMethods_Test3: self.EventMethods_Func3,  
                }  
    def EventMethods_Func1(self):  
        print ("use the EventMethods_Func1111" ) 
  
    def EventMethods_Func2(self):  
        print ("use the EventMethods_Func2222"  )
  
    def EventMethods_Func3(self):  
        print ("use the EventMethods_Func3333"  )
  
  
test=Test()  
test.EventMethods['func1']