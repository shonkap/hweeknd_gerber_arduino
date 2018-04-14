#### Calvin Gagliano, Gerber PCB Maker
#### April 14th, HWeekend
#### send_data.py
#### Sends data to Arduino after parsing Gerber file

# Import PySerial (for serial ports)
import serial

import time

# Set serial port to COM3 w/ 9600 bitrate
ser = serial.Serial('COM3', 9600)

# Open gerber file
file = open('gerber.gbr')

# Need parser

# Send 1 line at the time
while 1:
    line = file.readline()
    if not line:
        break
    ser.write(line)
    time.sleep(3)

file.close
