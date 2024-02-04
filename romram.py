# rshell -p /dev/tty.usbmodem1231401
# minicom -D /dev/tty.usbmodem1231401 -b 115200

from ansi import *
from machine import Pin
from utime import sleep

# Set the pins to correct values
def set_pins(pins, data):
    for pin in pins:
        this_bit = data & 0x01
        if(this_bit == 1):
            pin.on()
        else:
            pin.off()
        data = (data >> 1)

  
def io_pin_handler(p):
    if IOREQ.value()==False:
        print(top + down + "IO: ON")
    sleep(0.1) # wait for 0.1 second

def w_pin_handler(p):
    if WR.value()==False:
        print(top + down + "W: ON")
    sleep(0.1) # wait for 0.1 second

def r_pin_handler(p):
    if RD.value()==False:
        print(top + down + "R: ON")
    sleep(0.1) # wait for 0.1 second

# Clock Ticks
tick = 0

# ROM/RAM
ram_memory = []
for b in range(16384):
    ram_memory.append(0)

# LED status light
led_pin = Pin("LED", Pin.OUT)

# Write and Read signals
WR = Pin("GP0", Pin.IN)
#WR.irq(handler=w_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

RD = Pin("GP1", Pin.IN)
#RD.irq(handler=r_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# IO Request
IOREQ = Pin("GP27", Pin.IN, Pin.PULL_UP)
#IOREQ.irq(handler=io_pin_handler,trigger=Pin.IRQ_RISING)

# Memory Request
# MREQ = Pin("GP28", Pin.IN)
# MREQ.irq(handler=m_pin_handler,trigger=Pin.IRQ_RISING)

# Address Pins
address = []
address_pins = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]
print("Address pins 1-14")
for pin_number in address_pins:
    address.append(Pin(pin_number, Pin.IN, Pin.PULL_DOWN))

# Data pins
datavalues = []
data_pins = [16,17,18,19,20,21,22,26]
for pin_number in data_pins:
    datavalues.append(Pin(pin_number, Pin.OUT))

# Blink
print(clear)
print()
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

# Handle providing or writing data at an address
def romram(pin):
    global tick
    
    this_address = 0
    this_data = 0

    for address_pin in reversed(address):
         this_address = (this_address << 1) + address_pin.value()

    # When RD is low then z80 is reading
    is_reading = RD.value()
    if(is_reading == 0):
        
        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.OUT)
        set_pins(datavalues, ram_memory[this_address])
        this_data = ram_memory[this_address]

    # Assuming is writing    
    else:
        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.IN)
        for data_pin in reversed(datavalues):
            this_data = (this_data << 1) + data_pin.value()
            ram_memory[this_address] = this_data

    print(top)         
    print('{:8}'.format(tick), end='') 
    print(bold + " IO: " + reset  + str(IOREQ.value()),end='')
    print(bold + " RD: " + reset, is_reading, end='')
    print(bold + " WR: " + reset  + str(WR.value()), end='')
    print(bold + " Address: " + reset, '0x{:04x}'.format(this_address), end='')
    print(bold + " Data: " + reset, bin(this_data))
    
    print()  
    print(clearline)
    
    tick = tick + 1


# Clock
Clock = Pin("GP28", Pin.IN)
Clock.irq(handler=romram, trigger=Pin.IRQ_RISING)
