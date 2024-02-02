# rshell -p /dev/tty.usbmodem1231401
# minicom -D /dev/tty.usbmodem1231401 -b 115200

from machine import Pin
from utime import sleep

# ANSI
reset = "\u001b[0m"
bold = "\u001b[1m"
underline = "\u001b[4m"
reverse = "\u001b[7m"
clear = "\u001b[2J"
clearline = "\u001b[2K"
up = "\u001b[1A"
down = "\u001b[1B"
right = "\u001b[1C"
left = "\u001b[1D"
nextline = "\u001b[1E"
prevline = "\u001b[1F"
top = "\u001b[0;0H"

def gotoxy(x, y):
    return f"\u001b[{y};{x}H"

def m_pin_handler(p):
    if MREQ.value():
        led_pin.value(0)
    else:
        led_pin.value(1)
    sleep(0.1) # wait for 0.1 second
    
def io_pin_handler(p):
    if IOREQ.value()==False:
        print(top + down + "IO: ON")
    sleep(0.1) # wait for 0.1 second

def w_pin_handler(p):
    if MREQ.value()==False:
        print(top + down + "W: ON")
    sleep(0.1) # wait for 0.1 second

def r_pin_handler(p):
    if MREQ.value()==False:
        print(top + down + "R: ON")
    sleep(0.1) # wait for 0.1 second



# LED status light
led_pin = Pin("LED", Pin.OUT)

# Write and Read signals
WR = Pin("GP0", Pin.IN)
WR.irq(handler=w_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

RD = Pin("GP1", Pin.IN)
RD.irq(handler=r_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# IO Request
IOREQ = Pin("GP27", Pin.IN, Pin.PULL_UP)
IOREQ.irq(handler=io_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# Memory Request
MREQ = Pin("GP28", Pin.IN)
MREQ.irq(handler=m_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# Address Pins
print("Address pins 1-14")
A1 = Pin("GP2", Pin.IN)
A2 = Pin("GP3", Pin.IN)
A3 = Pin("GP4", Pin.IN)
A4 = Pin("GP5", Pin.IN)
A5 = Pin("GP6", Pin.IN)
A6 = Pin("GP7", Pin.IN)
A7 = Pin("GP8", Pin.IN)
A8 = Pin("GP9", Pin.IN)
A9 = Pin("GP10", Pin.IN) 
A10 = Pin("GP11", Pin.IN)
A11 = Pin("GP12", Pin.IN)
A12 = Pin("GP13", Pin.IN)
A13 = Pin("GP14", Pin.IN)
A14 = Pin("GP15", Pin.IN)

# Data pins
D1 = Pin("GP16", Pin.OUT)
D2 = Pin("GP17", Pin.OUT)
D3 = Pin("GP18", Pin.OUT)
D4 = Pin("GP19", Pin.OUT)
D5 = Pin("GP20", Pin.OUT)
D6 = Pin("GP21", Pin.OUT)
D7 = Pin("GP22", Pin.OUT)
D8 = Pin("GP26", Pin.OUT)

# Set to NOP
D1.value(0)
D2.value(0)
D3.value(0)
D4.value(0)
D5.value(0)
D6.value(0)
D7.value(0)
D8.value(0)




# Blink
print(clear)
print("Boot",end='')
sleep(2)
print(" ",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".",end='')
sleep(0.1)
print(".")
sleep(0.1)
print(clear)

while True:
    
    print(top)
    
    print(bold + "MR:" + reset + str(MREQ.value()),end='')
    print(bold + " IO:" + reset  + str(IOREQ.value()),end='')
    print(bold + " RD:" + reset  + str(RD.value()),end='')
    print(bold + " WR:" + reset  + str(WR.value()),end='')
    print(bold + " ADDR: " + reset , end='')
    
    print(int(A8.value()),end='')
    print(int(A6.value()),end='')
    print(int(A5.value()),end='')
    print(int(A4.value()),end='')
    print(int(A3.value()),end='')
    print(int(A2.value()),end='')
    print(int(A1.value()))
    print(clearline)
    

