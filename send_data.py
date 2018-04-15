#### Calvin Gagliano, Gerber PCB Maker
#### April 14th, HWeekend
#### send_data.py
#### Sends data to Arduino after parsing Gerber file

def parse(line):
    #Three modes: D01, D02, and D03
        # D01 is pen down mode
        # D02 is pen up mode
        # D03 makes a dot
    #Typically the format for these commands are:
        # X(# of dig_int)(# of dig_dec)Y(# of dig_int)(# of dig_dec)D0(command)*
    #First, extrapolate the command
    data.append(get_command(line));
    #If it didn't have a command, get next line
    if data[0] == 1:
        return 1
    #Extrapolate the X coordinate
    xindx = line.find('X');
    xcoord = ""
    while line[xindx+1] in range(0, 9):
        xcoord = xcoord + line[xindx+1]
        xindx += 1



def get_command(line):
    if "D01" in line:
        return "D01"
    elif "D02" in line:
        return "D02"
    elif "D03" in line:
        return "D03"
    # fail
    else:
        return 1

# Import PySerial (for serial ports)
import serial
import sys
import time

# Set serial port to COM3 w/ 9600 bitrate
ser = serial.Serial("COM3", 9600)

# Open gerber file
file = open("gerber.gbr", 'r')

# Parse starter
startParse = False
dig_int = 0
dig_dec = 0

# Data to send Arduino
data = []

# Send 1 line at the time
while 1:
    # Read line
    line = file.readline()

    # Check
    x = 0

    # If end of file, quit and close file
    if not line:
        break

    # Start parser
    if startParse == True:
        x = parse(line)

    # Check for failure
    if x == 1:
        data = []
    else:
        #ser.write(data)

    # Find # of integer/decimal digits, begin parser
    # The line that defines this is typically at the top and is
    # %FSLAX(dig_int)(dig_dec)Y(dig_int)(dig_dec)*%

    # Sleep for 3 milliseconds
    time.sleep(3)

file.close
