# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 21:40:02 2017

@author: rain
"""
from random import randint
class 人:
    def __init__(self,name="我"):
        self.名字=name
        self.key=randint(0,1000)
        self.keys=[i for i in range(10)]
    def addkey(self,key):
        self.keys.append(key)
    def getkey(self):
        return self.key
    def 发现(self):
        return True
    def 身影(self):
        return self.key
    def 看见(self):
        
        nlist=["甲","乙","丙","张三","李四","王五"]
        saylist=[
        "我突觉得今天天气不做，然后我走了",
        "我突然饿了，然后去吃饭了",
        "么啥事情，我走了",
        "天黑了，回家",
        "妈妈喊我回家吃饭了，然后回家了",
        "在秋分萧瑟中，默默的回家了"
        ]
        print(self.名字+"看到了"+nlist[randint(0,len(nlist)-1)]+"站在那里时,"\
        +saylist[randint(0,len(saylist)-1)])
        index=randint(0,len(self.keys)-1)
        return self.keys[index]   
    def 会说(self,string):
        print(self.名字+"会说"+string)
    

if __name__=="__main__":   
    我=人("我")
    你=人("你")
    我.addkey(你.getkey())
    while(我.发现()):
        if(我.看见()==你.身影()):
            我.会说("你若安好，便是晴天")
            break
        
    print("""
       ***            ***
     **    **      **     **
   **        **  **         **
 **     这个故事  告诉我们，  **
 **     除非她  足够信任你，  **
  **    给你  家门钥匙。     **
   **   否则无  谓的等待,   **
    **  只会让你  陷入死循环的。
      **                 **
       ***              **
          **          **
             **     **
                **
    """)