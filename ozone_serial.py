#  communicates with ozone monitor over virtual COM to ethernet to rs232
"""
Created on Wed Oct 11 15:54:29 2017

@author: paltryore
"""

import serial

## Serial port configuration
ser = serial.Serial()
ser.port ='COM2'
ser.baudrate = 2400

# defaults:
# bytesize = 8
# parity = 'N'
# stopbits = 1

# timeout = None
# xonxoff = 0
# rtscts = 0


## data structure configuration
filename = "pyserial.log"


ser.open()
port_status = ser.is_open

while port_status == True:
    line = ser.readline().decode("utf-8").rstrip() # this command won't finish until it reads a '\n'
    print(line)
    with open(filename, 'a+') as f:
        f.write(line+"\n")

## Other notes:
# s = ser.read(100) # read up to 100 bytes

ser.close()

