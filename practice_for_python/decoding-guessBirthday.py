# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script file for encoding guestBirthday game.
"""
"""
l1=[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31]
l2=[2,3,6,7,10,11,14,15,18,19,22,23,26,27,30,31]
l3=[4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31]
l4=[8,9,10,11,12,13,14,15,24,25,26,27,28,29,30,31]
l5=[16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
ll=(l1,l2,l3,l4,l5)"""
def myprint(mylist):
    for i in range(len(mylist[0])):
        print(
        format(mylist[0][i],"5b")+'      '+ format(mylist[1][i],"5b")+'      '+\
        format(mylist[2][i],"5b")+'      '+ format(mylist[3][i],"5b")+'      '+\
        format(mylist[4][i],"5b")
        )
trick=[1,2,4,8,16]
printlist=[]
num=-1
mylist=[]
for i in range(5):   
    printlist=[]
    num=-1
    isum=0
    for j in range(16):
        num=trick[i]+j+isum
        if num>=trick[i]:
            if format(num,"b").zfill(5)[4-i]=='0':  
                num=num+trick[i]
                isum=isum+trick[i]
        printlist.append(num)
    mylist.append(printlist)
    print(printlist)
    
myprint(mylist)

        