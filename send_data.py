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
    #Get index of where "X" is
    xindx = line.find('X');
    xcoord = "X"
    #If 'X' exists in the line
    if xindx != -1:
        # If it's a digit or a negative sign
        while line[xindx+1].isdigit() or line[xindx+1] == '-':
            # Add it to overall string to be transferred
            xcoord = xcoord + line[xindx+1]
            xindx += 1
        # If the line is not empty
        if xcoord != "":
            data.append(xcoord)

    #Extrapolate the Y coordinate
    # Get index of "Y"
    # Same thing for Y coordinate
    yindx = line.find('Y');
    ycoord = "Y";
    #If 'Y' exists in the line
    if yindx != -1:
        # While the next character is a number or negative
        while line[yindx+1].isdigit() or line[yindx+1] == '-':
            ycoord = ycoord + line[yindx+1]
            yindx += 1
        if ycoord != "":
            data.append(ycoord)

    return 0

def get_command(line):
    # Find Command in line
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
ser = serial.Serial("COM3", 9600,timeout=5)
print("Opening connection with COM3, 9600 bitrate")

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
    print(line);

    # Check
    x = 0

    # If end of file, quit and close file
    if not line:
        break

    if get_command(line) != 1:
        startParse = True

    # Start parser
    if startParse == True:
        x = parse(line)

    # Check for failure
    if x == 1:
        data = []

    # Sends data to Arduino by converting to binary.
    # First, combine data together.
    # If X/Y coord is missing, just send the one is there.
    fulldata = ""
    for z in range(0, len(data)):
        fulldata = fulldata + data[z]

    if fulldata != "":
        ser.write(str.encode(fulldata))
        time.sleep(6)
        # Wait for Arduino buffer
        # Grab message that Arduino sends (just same as input for now)
        msg = ser.readline(ser.inWaiting())
        print("From Arduino: ")
        print(msg.decode())

    data = []

    # Find # of integer/decimal digits, begin parser
    # The line that defines this is typically at the top and is
    # %FSLAX(dig_int)(dig_dec)Y(dig_int)(dig_dec)*%

    # Sleep for .3 seconds
    time.sleep(1)

ser.write(str.encode("done"))
time.sleep(6)
msg = ser.readline(ser.inWaiting())
print("From Arduino: ")
print(msg.decode())
time.sleep(10)
msg = ser.readline(ser.inWaiting())
print("From Arduino: ")
print(msg.decode())
file.close
