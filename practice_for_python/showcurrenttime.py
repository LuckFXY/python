# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 18:46:57 2017

@author: rain
"""

import time
currentTime=time.time()
totalSeconds=int(currentTime)
currentSecond=totalSeconds%60
totalMinutes=totalSeconds//60
currentMinute=totalMinutes%60
totalHours=totalMinutes//60
currentHour=totalHours%24
totalDays=totalHours//24
print ('GMT: ',currentHour,currentMinute,currentSecond)