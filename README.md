# ozone-monitor
Processing data output from a <a href="http://www.twobtech.com/model-106-l.html">2B Technologies 106-L Ozone Monitor</a> with Python 3.

The 106-L outputs data through a serial port every 10 seconds in a single line:
```shell
Ozone(ppb),Cell temp, Cell pressure, Flow rate, Photodiode Voltage, Date (DD/MM/YY), Time (HH:MM:SS)
```

I am using <a href="https://pythonhosted.org/pyserial/">pySerial</a> in ozone_serial.py to read and temporarily log data, and Windows task scheduler to call ozoneoutput3.pyw. 

ozoneoutput3.pyw reads the log file, checks for errors, and writes ozonetemp.log

ozonescript3.pyw reads ozonetemp.log, averages the readings, appends to the daily log, creates graphs with matplotlib, and calls a WinSCP batch script to synchronize to a server that hosts the page.

Converting this:
```shell
11.3,24.4,950.2,1430,1.233,04/05/17,07:14:34
13.2,24.5,950.4,1429,1.234,04/05/17,07:19:34
11.2,24.5,950.5,1426,1.234,04/05/17,07:20:34
```

Into this:

<img src="https://raw.githubusercontent.com/paltryore/ozone-monitor/master/ozonetoday.png">

And this:
```shell
11.3,24.4,950.2,1430,1.233,2017-05-04,07:14:34
13.2,24.5,950.4,1429,1.234,2017-05-04,07:19:34
11.2,24.5,950.5,1426,1.234,2017-05-04,07:20:34
```
