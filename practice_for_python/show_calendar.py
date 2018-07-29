# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 10:26:26 2017

@author: rain
"""

def weekOfFirstDay(inputYear=2017,inputMonth=3,printAll=True):
    START_YEAR=1
    WEEK_OF_START_YEAR=1#MONDAY
    assert(inputYear>=START_YEAR)
    leap_year=0
    
    diffOfYear=inputYear-START_YEAR
    leap_year+=diffOfYear//400
    divisible_4=diffOfYear//4
    divisible_100=diffOfYear//100
    leap_year+=divisible_4-divisible_100
    if(diffOfYear%4!=0):
        diff=inputYear-START_YEAR
        for year in range(inputYear-diff,inputYear):
            if printAll:
                print (year,end='|')
        leap_year+=1 \
        if (year%4==0 and year%100!=0)or(year%400==0) else 0

    Febuary=29\
        if (inputYear%4==0 and inputYear%100!=0)or(inputYear%400==0) else 28

    DaysOfMonth=[31,Febuary,31,30,31,30,31,31,30,31,30,31]
    #the number of days until the inputMonth in InputYear
    DaysUIMIY=sum([DaysOfMonth[i] for i in range(inputMonth-1)])
    #print(DaysUIMIY,end=':')
    diff_days=diffOfYear*365+leap_year+DaysUIMIY
    week=(diff_days+WEEK_OF_START_YEAR)%7
    if printAll:
        print("%d/%d :%d"%(inputYear,inputMonth,week))
    else:
        return week,DaysOfMonth[inputMonth-1]
#weekOfFirstDay(1973,1)
 
def test(): 
    #just for test
    import datetime
    for year in range(1,2017):
        print(year,end=' ')
        for month in range(1,13):
            week_True=datetime.datetime(year,month,1).strftime("%w")
            week_Test,DaysOfMonth=weekOfFirstDay(year,month,False)
            if(str(week_Test)==week_True):
                print('.',end='')
            else:
                print('\n',year,month,'wrong!',week_Test,week_True)
        if(year%4==0):
            print()

def printline(length,content=''):
    assert type(content)==str
    assert type(length)==int
    numOfBlank=length-len(content)
    flag=numOfBlank%2==1
    numOfBlank=numOfBlank//2
    for i in range(numOfBlank):
        print('-',end='')
    print(content,end='')
    if flag:
        print(' ',end='')
    for i in range(numOfBlank):
        print('-',end='')
    print() 
    
def showCalender(year,month):
    chr_month=['January','February','March','April',
              'May','June','July','August','September',
              'Octer','November','December']
    chr_week=['Sunday','Monday','Tuesday','Webnesday',
              'Thursday','Friday','Saturday']
    printline(50,chr_month[month]+' '+str(year))  
    print('    ',end='')
    for i in range(7):
        print(chr_week[i][:3],end='    ')
    print()
    week,DaysOfMonth=weekOfFirstDay(year,month,False)
    mylist=['' for i in range(week)]
    mylist+=[i for i in range(1,DaysOfMonth+1)]    
    print('    ',end='')
    for i in range(1,len(mylist)+1):
        print(format(str(mylist[i-1]),"7s"),end='')
        if i%7==0:
            print()
            print('    ',end='')

if __name__=='__main__':
    showCalender(2017,3)
    #test()