from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import os
from hashlib import md5
import time


if os.path.exists("data") == False:
    os.mkdir("data")

def getImg(html_text):
    imglist=re.findall('img src="(http.*?)"',html_text)
    return imglist

def getbsObj(url):
    bsObj=None
    html_text=None
    hash_name=md5(url.encode('utf-8')).hexdigest()
    filename = "data" + "/" + str(hash_name)
    count=0
    MAXTIME=5

    if os.path.exists(filename):
        print(url+" was found in cache folder")
        with open(filename,"r",encoding="utf8") as infile:
            html_text=infile.read()
        pass #open cache if it is exists
    else:
        while (html_text == None and count < MAXTIME):
            count+=1
            try:
                html=urlopen(url)
                html_text = html.read().decode("utf-8", errors="ignore")
            except (HTTPError,URLError) as e:
                print(e)
                print("wait")
                time.sleep(5)
                print("try again "+str(count))
            except ValueError as e2:
                print(e2)
                return

        print(len(html_text))
        with open(filename,"w",encoding="utf8") as outfile:
            outfile.write(html_text)

    try:
        bsObj=BeautifulSoup(html_text,"html5lib")
        #title=bsObj.body.h1
        #print(title)
    except AttributeError as e:
        print("cannot create the bsObj")


    return bsObj

url="http://www.en8848.com.cn/kaoyan/zw/zuowen155/179046.html"
bsObj=getbsObj(url)
#if bsObj!=None:
composition_list=bsObj.findAll("a",title=re.compile(u"考研英语作文[\u4e00-\u9fa5]+"))



def getComposition(href,filename):
    h2=getbsObj(href)
    title=None
    if h2==None:
        print("cannot reach "+href)
        return
    describe=h2.find("div",{"class":"describe_text","id":"dete"} )
    if describe==None:
        describe = h2.find("div",{"id": "dete"})
    try:
        title=[i for i in describe.stripped_strings]
    except AttributeError:
        print("cannot find describe")
        return
    #print(title[0])
    output=[]

    output.append(title[0]+"\n")
    articlebody=h2.find("div",{"id":"articlebody"})
    #print(articlebody)
    for item in articlebody.findAll("p"):
        if item.find("img")!=None:
            continue
        inside=item.find("strong")
        if inside!=None:
            item=inside
        essay=item.contents
        for e in essay:
            e=str(e).replace("<br/>","")
            if e!="":
                #print(e)
                output.append(e+"\n")
    print(title)
    with open(filename,"w",encoding="utf8") as f:
        f.writelines(output)


for i in range(len(composition_list)):
    one = composition_list[i]
    href = one.get("href")
    if href.find("en8848"):
        filename=str(i)+'.txt'
        getComposition(href,filename)
