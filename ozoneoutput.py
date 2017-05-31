# -*- coding: utf-8 -*-
"""
Created on Mon May 08 14:12:57 2017

@author: paltryore
"""
# activated by windows task manager
# reads data from teraterm.log.1 every minute and appends it to ozonetemp.log
# every 15 minutes, the other ozone script reads ozonetemp.log to average the data and then deletes ozonetemp.log

import os

filename = "teraterm.log.1"

with open("date.cfg") as f:
        currentDay=f.read()
        
with open(filename, 'r+') as f:
    linesRaw = f.read().splitlines() # linesraw is an array of strings. Each string is one line from the file

lines = []

for i in range(len(linesRaw)):
    lines.append(linesRaw[i].strip().split(','))
# error handling:
    if len(lines[-1])!=7:
        lines.pop(-1) #remove latest item b/c log line only contained portion of entry
    elif len(lines[-1][6])!=8:
        lines.pop(-1)
    else:
        try:
            testozone = float(lines[-1][0])
        except:
            lines.pop(-1)
date = "20"+lines[-1][5][6:8]+"-"+lines[-1][5][3:5]+"-"+lines[-1][5][0:2]
    #convert date to ISO 8601
if date != currentDay: #run script to clear out data from previous day
    os.system("python ozonescript1.5.py")
    with open("date.cfg","w") as f:
        f.write(date)

print lines
    
with open("ozonetemp.log", 'a+') as f:
    for i in lines:
        #if float(i[0]) < 0 or float(i[0])>
        for j in range(5):
            f.write(i[j]+',')
        f.write(date+','+i[6]+'\n')
