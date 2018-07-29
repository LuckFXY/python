# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 23:25:51 2017

@author: rain
"""

import sqlite3
import os

if os.path.exists('mydata.db')==False:
    conn=sqlite3.connect('mydata.db')
    c= conn.cursor()
    
    c.execute('''
              CREATE TABLE data
              (filename text,
              InCir_R int,InCir_X int, InCir_Y int,
              OutCir_R int,OutCir_X int, OutCir_Y int)
              ''')
    c.execute("INSERT INTO data VALUES ('1.bmp',1,2,3,4,5,6)")
    conn.commit()
    conn.close()
    
t=('4.bmp',)
conn=sqlite3.connect('mydata.db')
c= conn.cursor()
#c.execute("INSERT INTO data VALUES ('4.bmp',1,2,3,4,5,6)")
#c.execute("INSERT INTO data VALUES ('2.bmp',1,2,3,4,5,6)")
#c.execute("INSERT INTO data VALUES ('3.bmp',1,2,3,4,5,6)")
newone=(100,'2.bmp')
#c.execute("update data set InCir_R = ? where filename = ?",newone)
block=[10,20,30,40,50,60]
block.append(t[0])
'''
c.execute("update data set \
                  InCir_R = ?, \
                  InCir_X = ?, \
                  InCir_Y = ?, \
                  OutCir_R = ?, \
                  OutCir_X = ?, \
                  OutCir_Y = ? \
                  where filename = ?",block)
result=[i for i in c.execute('select * from data where filename=?',t)]
r=c.execute('select * from data where filename=?',t)
'''
#c.execute("Alter TABLE data RENAME TO data_old")
#root=''
#c.execute("INSERT INTO data VALUES (?,0,0,0,0,0,0",(root))
for row in c.execute('select filename from data'):
    print(row)
#c.execute("Alter TABLE data_old RENAME TO data")
conn.commit()
conn.close()

