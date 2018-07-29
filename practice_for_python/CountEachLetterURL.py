# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 21:14:50 2017

@author: rain
"""
import os
import urllib.request
def countLetters(s,mydict):
    for ch in s:
        if ch not in mydict:
            mydict[ch]=1
        else:
            mydict[ch]+=1
def main():
    #url=input("Enter a URL for a file : ").strip()
    if os.path.isfile("Lincoln1.txt")==False:
        url="http://cs.armstrong.edu/liang/data/Lincoln.txt"
        url="http://jingyan.baidu.com/article/e5c39bf56349af39d760333d.html"
        #url=input("Enter a URL for a file : ").strip()
        try:
            infile=urllib.request.urlopen(url)
            s=infile.read().decode() #read the content as string
            fp=open("Lincoln.txt","w")
            fp.write(s)
            fp.close()
        except IOError:
            print("The website of %s is no exist or no response"%(url))
    else:
        fp=open("Lincoln.txt","r")
        s=fp.read()
        fp.close()
    #print(s)
    mydict={}
    countLetters(s,mydict)
    
    fp=open("baidubaike.txt","w")
    mylist_sorted=sorted(mydict.items(),key=lambda item:item[1],
                         reverse=True)
    for tup in mylist_sorted:
        
        mystr=str(tup[0])+" appears "+str(tup[1])+\
              str(" time" if tup[1]==1 else " times")+'\n'
        fp.write(mystr)
    
    fp.close()
    print("The program is over")
                
main()