# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 23:25:51 2017

@author: rain
"""

import sqlite3
import os

if os.path.exists('example.db')==False:
    conn=sqlite3.connect('example.db')
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
    
t=('2.bmp',)
conn=sqlite3.connect('example.db')
c= conn.cursor()
#c.execute("INSERT INTO data VALUES ('4.bmp',1,2,3,4,5,6)")
#c.execute("INSERT INTO data VALUES ('2.bmp',1,2,3,4,5,6)")
#c.execute("INSERT INTO data VALUES ('3.bmp',1,2,3,4,5,6)")
newone=(100,'2.bmp')
c.execute("update data set InCir_R = ? where filename = ?",newone)
#for row in c.execute('select * from data where filename=?',t):
for row in c.execute('select * from data'):
    print(row)
conn.commit()
conn.close()

