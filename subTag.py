# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:09:36 2017

@author: rain
"""
import os
os.chdir("f:/python_practice/WebScraping")
from bs4 import BeautifulSoup
import commfunc as cf
import re
if __name__=="__main__":
    #html_addr="http://www.pythonscraping.com/pages/page3.html"
    #bsObj=cf.get_bsObj(html_addr)
    soup=BeautifulSoup(open("page3.html"),"lxml")
    
    if soup!=None:
        #--------------------------------------------------------
        
        #the return of findAll is a list of result
        #gift_table=soup.findAll("table",{"id":"giftList"})
        #the return of find is result directly
        #for child in soup.find("table",{"id":"giftList"}).children:
        #    print(child)
        
        #print("-----------------------------------------")
        #for sibling in gift_table[0].tr.next_siblings:
        #    print(sibling)
        #--------------------------------------------------------
        rr=re.compile("\.\/page3_files\/img.*\.jpg")    
        for img in soup.findAll("img",{"src":rr}):
            print(img.parent.previous_sibling.get_text())
        #--------------------------------------------------------
        