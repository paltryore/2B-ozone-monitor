# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 17:08:25 2017

@author: paltryore
"""

# 2B Technologies 106L Ozone monitor records data for each interval as single line:
# Ozone(ppb),Cell temp, Cell pressure, Flow rate, Photodiode Voltage, Date, Time
# 21.7,46.8,930.2,1496,1.741,27/04/17,15:02:34

# Update Log
## 1.0 - loads data from teraterm log, makes graph and cleaner log file
## 1.1 - loads data also from previously in current day for graph
## 1.2 - uses time instead of decimal hours. fixed issues from 1.1
## 1.3 - added currentozone.png for website
## 1.4 - added findXdayhigh; 7dayhigh.png,30dayhigh.png
## 1.5 - added 15 minute averaging

import matplotlib.pyplot as plt # Makes MATLAB-like graphs
import shutil # copy files
from datetime import datetime,timedelta # python handling HH:MM:SS
import numpy as np

def findXdayhigh(currentDay,X): # checks ozone logs from past X days to find the highest ozone value. 
    # returns ['YYYY-MM-DD','HH:MM:SS', float(ozone in ppb)]
    Xdayhigh = [0,0,0]
    Dayformatted = datetime.strptime(currentDay,"%Y-%m-%d")
    for i in range(X):
        targetDay1= Dayformatted - timedelta(days=i)
        targetDay2=targetDay1.strftime('%Y-%m-%d')
        data = []
        try:
            with open("ozone/ozone-"+targetDay2+".log") as f:
                lines=f.read().splitlines()
            for i in range(len(lines)):
                data.append(lines[i].strip().split(','))
            for i in data:
                if float(i[0])>Xdayhigh[2]:
                    Xdayhigh=[i[5],i[6],float(i[0])]
        except:  print "No data from "+targetDay2
    date = Xdayhigh[0][0:10]
    return [date,Xdayhigh[1],Xdayhigh[2]]

def main(filename):
    olddata = []
    data = [] # data will hold the values extracted from the ozone monitor log. [[date1,time1,ozone1],[date2,time2,ozone2]]
#    prevdata = [] # prevdata will hold values from the finished day if the collected data passes midnight
    lines = []
#    x=0 # when data passes midnight, x equals number of entries from the previous day. used to handle data processing loop below.
#   datecheck=False
    archive = True    
    with open("date.cfg") as f:
        currentDay=f.read()
    date=currentDay
        
    try: # open data archive from previously in the day, if exists, load into data
        with open("ozone/ozone-"+currentDay+".log") as f: 
            print "loaded ozone/ozone-"+currentDay+".log"
            oldlines = f.read().splitlines()
        for i in range(len(oldlines)):
            olddata.append(oldlines[i].strip().split(','))
            time = olddata[i][6][0:8]
            date = olddata[i][5][0:10]
            data.append([date,time,float(olddata[i][0])])
    except:
        print "No previous data from "+currentDay
    


    with open(filename, 'r+') as f:
        linesRaw = f.read().splitlines() # linesraw is an array of strings. Each string is one line from the file
        f.seek(0)
        f.truncate() # deletes all lines in the output file to keep it from growing too large
   

        
    for i in range(len(linesRaw)):
        lines.append(linesRaw[i].strip().split(','))
        #if datecheck==True:
#            print i,x
#            print lines
        print len(lines[i]), lines[i]
##        # error handling:
##        if len(lines[-1])!=7:
##            lines.pop(-1) #remove latest item b/c log line only contained portion of entry
##        else:    
##            try:
##                testtime = datetime.strptime(lines[-1][6],"%H:%M:%S")
##            except:
##                lines.pop(-1)
##            try:
##                testozone = float(lines[-1][0])
##            except:
##                lines.pop(-1)
        
        date = lines[i][5][0:10]
#        if date == currentDay:
        
#        else:
#            prevdata = data
#            data = []
#            data.append([date,time,float(lines[i-x][0])])
#            oldLines=lines[:-1] # don't include first entry of new day
#            lines=[lines[-1]] # update lines to only hold first entry of new day
##            print lines
#            currentDay=date
##            datecheck=True
#            x=i
    # Average over all input lines
    sumdata = [0,0,0,0,0]
    average = [False,False,False,False,False]
    for i in lines:
        for j in range(5):
            sumdata[j] += float(i[j])
    for j in range(5):
        average[j] = round(sumdata[j] / len(lines),3)
    median = int(len(lines)/2)
    print 'median'+str(median)
    time = lines[median][6]
    data.append([date,time,average[0]])
  
    # Archive Data, appending if file already exists
    if archive == True:
        with open("ozone/ozone-"+date+".log", "a+") as f:
            for i in range(5):
                f.write(str(average[i])+',')
            f.write(date+','+lines[median][6]+'\n')
    
#    if prevdata != []:
#        with open("ozone/ozone-"+prevdata[-1][0]+".log", "a+") as f:
#            for i in oldLines:
#                for j in range(5):
#                    f.write(i[j]+',')
#                f.write(prevdata[-1][0]+','+i[6]+'\n')


            
    # Make today's graph
    t1 = []
    ozone = []
    print "graphed data:"
    for i in data:
        print i
        t1.append(datetime.strptime(date+"-"+i[1],"%Y-%m-%d-%H:%M:%S"))
        ozone.append(i[2])
    t=np.array(t1)
#    plt.figure(1)
    plt.plot(t,ozone)
    
        # set graph axis limits to midnight-midnight; -5 to 60 ppb
    plt.axis([datetime.strptime(date+"-00:00:00","%Y-%m-%d-%H:%M:%S"),datetime.strptime(date+"-23:59:59","%Y-%m-%d-%H:%M:%S"),-5,60])
    plt.xlabel('local time')
    plt.ylabel('Ozone (ppb)')
    plt.title('Ozone Concentration, '+date)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("ozone/ozonetoday.png")
#    plt.show()
    plt.clf()

    # Make website files
    ## graph already made above: "ozone/ozonetoday.png"

    ## current ozone value:
    #with open("currentozone.txt",'w+') as f: 
    #    f.write(str(data[-1]))
    color1='k' # default color = black
    plt.figure(2, figsize=(7,1) )
    currentozone = round(data[-1][2],0)
    if currentozone > 70: # ozone exposure above 70 ppb for 8 hours is unhealthy for sensitive groups
        color1='r'
    elif currentozone > 50: # ozone exposure above 50 ppb for 8 hours is "moderate" air quality
        color1='y'
    else:
        color1='g' # ozone below 50 ppb is "good" air quality
    plt.text(0.5,0.5,'Current Ozone ('+date+' '+time[0:5]+'): '+str(currentozone)+' ppb', horizontalalignment='center',color=color1, verticalalignment='center', fontsize=15)
    plt.axis('off')
    plt.savefig('ozone/currentozone.png')

    ## 7-day high
    dayhigh7 = findXdayhigh(currentDay,7)
    color1='k' # default color = black
    plt.figure(3, figsize=(7,1) )
    highozone = round(dayhigh7[2],0)
    if highozone > 70: # ozone exposure above 70 ppb for 8 hours is unhealthy for sensitive groups
        color1='r'
    elif highozone > 50: # ozone exposure above 50 ppb for 8 hours is "moderate" air quality
        color1='y'
    else:
        color1='g' # ozone below 50 ppb is "good" air quality
    plt.text(0.5,0.5,'7 day high ('+dayhigh7[0]+' '+dayhigh7[1][0:5]+'): '+str(highozone)+' ppb', horizontalalignment='center',color=color1, verticalalignment='center', fontsize=15)
    plt.axis('off')
    plt.savefig('ozone/7dayhigh.png')
    
    dayhigh30 = findXdayhigh(currentDay,30)
    color1='k' # default color = black
    plt.figure(4, figsize=(7,1) )
    highozone = round(dayhigh30[2],0)
    if highozone > 70: # ozone exposure above 70 ppb for 8 hours is unhealthy for sensitive groups
        color1='r'
    elif highozone > 50: # ozone exposure above 50 ppb for 8 hours is "moderate" air quality
        color1='y'
    else:
        color1='g' # ozone below 50 ppb is "good" air quality
    plt.text(0.5,0.5,'30 day high ('+dayhigh30[0]+' '+dayhigh30[1][0:5]+'): '+str(highozone)+' ppb', horizontalalignment='center',color=color1, verticalalignment='center', fontsize=15)
    plt.axis('off')
    plt.savefig('ozone/30dayhigh.png')
    
    

    ## daily ozone log
    if archive==True: shutil.copy2("ozone/ozone-"+date+".log","ozone/ozonetoday.log")
    
    # WinSCP monitors the Desktop/ozone folder for changes and automatically uploads to server
        
filelist=["ozonetemp.log"]

for i in filelist: 
    main(i)
    
