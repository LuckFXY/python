# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 17:53:10 2017

@author: rain
"""

"""
the last i value is slightly larger than 1,
so the last i value not to be add into sum
"""
sum=0
i=0.01
j=0
while i<=1.0:
    sum+=i
    j+=1
    i+=0.01    
print(i,' ',sum)
'''
    suppose that the tuition for a university is 10000 this year 
and increase 7% every year.
    In how mnay years will the tuition have doubled
'''
year=0
tuition=10000
increase=1.07
aim=tuition*2
while(tuition<aim):
    year+=1
    tuition*=increase
print ('year=',year,' tuition=',tuition)