# rshell -p /dev/tty.usbmodem1231401
# minicom -D /dev/tty.usbmodem1231401 -b 115200

import sys
from ansi import *
import machine
from machine import Pin, Timer
from utime import sleep

machine.freq(270000000)
print(machine.freq())

is_IO = False
is_reading = False
is_writing = False   
this_address = 0
this_data = 0

# Address Pins
address = []
address_pins = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]
for pin_number in address_pins:
    address.append(Pin(pin_number, Pin.IN))

# Data pins
datavalues = []
data_pins = [16,17,18,19,20,21,22,26]
for pin_number in data_pins:
    datavalues.append(Pin(pin_number, Pin.OUT))

# Write and Read signals
Clock = Pin("GP28", Pin.OUT)
Clock_Timer = Timer()
WR = Pin("GP0", Pin.IN, Pin.PULL_UP)
RD = Pin("GP1", Pin.IN, Pin.PULL_UP)

# IO Request
IOREQ = Pin(27, Pin.IN, Pin.PULL_UP)


# LED status light
led_pin = Pin("LED", Pin.OUT)

# Clock Ticks
tick = 0

# ROM/RAM
ram_memory = [ 
    
    0x3E, 0x48,       	#LD A,48H ("H")
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x45,       	#LD A,45H ("e")
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x4C,       	#LD A,4CH
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x4C,       	#LD A,4CH
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x4F,       	#LD A,4FH
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x20,       	#LD A,20H
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x57,       	#LD A,57H
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x4F,       	#LD A,4FH
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x52,       	#LD A,52H
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x4C,       	#LD A,4CH
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x44,       	#LD A,44H
    0xD3, 0x0A,       	#OUT (0AH),A
    0x3E, 0x21,       	#LD A,21H
    0xD3, 0x0A,       	#OUT (0AH),A
    0xC3, 00, 00,     	#JP 0000
    0x76              	#HALT

]

print("Booting")

# Get the address pins
def get_address():
    global tick, is_IO, is_reading, is_writing, this_address, address, this_data, datavalues, ram_memory
    this_address = 0
    for address_pin in reversed(address):
         this_address = (this_address << 1) + address_pin.value()
         
    #print(this_address)     
    return this_address

# Set the pins to correct values
def set_pins(pins, data):
    
    global tick, is_IO, is_reading, is_writing, this_address, address, this_data, datavalues, ram_memory
    
    for pin in pins:
        this_bit = data & 0x01
        if(this_bit == 1):
            pin.on()
        else:
            pin.off()
        data = (data >> 1)
        #print(data)

# Output the Z80 values
def print_status():
    global tick, is_IO, is_reading, is_writing, this_address, address, this_data, datavalues, ram_memory

    # Check if IO
    is_IO = (IOREQ.value()==0)

    # When RD is low then z80 is reading
    is_reading = (RD.value()==0)

    # Check if is writing
    is_writing = (WR.value()==0)
    
    # Get the address and the data for it
    this_address = get_address()
    this_data = ram_memory[this_address]

    #print(top)         
    print('{:8}'.format(tick), end='') 
    print(bold + " IO: " + reset, abs(is_IO),end='')
    print(bold + " RD: " + reset, abs(is_reading), end='')
    print(bold + " WR: " + reset, abs(is_writing), end='')
    print(bold + " Address:" + reset + " {:#018b}".format(this_address), end='')
    print(bold + " Data:" + reset + " {:#010b}".format(this_data), end='')
    print(" {:#06x}".format(this_data), reset, end='')
    
    if this_data < 126 and this_data >= 32:
        print(chr(this_data), end='')
    else:
        print("", end='')
    
    print()  
    #print(clearline)


# Write handler
def wr_handler(pin):
    global tick, is_IO, is_reading, is_writing, this_address, address, this_data, datavalues, ram_memory
    
    # NOT IO so is writing to memory
    if(IOREQ.value()==1):
        this_address = get_address()
        # WAIT.value(0)
        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.IN)
        for data_pin in reversed(datavalues):
            this_data = (this_data << 1) + data_pin.value()
            try:
                ram_memory[this_address] = this_data
            except:
                print("OOPS! Requested to write ", this_address)
            
        # WAIT.value(1)
        print_status()
        tick = tick + 1

# Read handler
def rd_handler(pin):

    global tick, is_IO, is_reading, is_writing, this_address, address, this_data, datavalues, ram_memory

    #print("IO :",IOREQ.value())

    # Not IO - Reading from memory
    if(IOREQ.value()==1): 
        
        this_address = get_address()

        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.OUT)
            
        
        this_data = ram_memory[this_address]
        set_pins(datavalues, this_data)

        #print(this_data)

        print_status()
        tick = tick + 1

# IO Handler
def io_handler(pin):

    global tick, is_IO, is_reading, is_writing, this_address, address, this_data, datavalues, ram_memory  
    print_status()
    tick = tick + 1

# Handle clock ticks
def clock_tick(timer):
    
    global tick
    led_pin.value(1)
    Clock.toggle()
    sleep(0.1)
    led_pin.value(0)
    tick = tick + 1
    if(RD.value()==0): rd_handler(RD)    
    if(WR.value()==0): wr_handler(WR)
    if(IOREQ.value()==0): io_handler(IOREQ)  

# Fill rest of the 8kb with NOP
# 8kb = 8181
# 16kb = 16382
for b in range(16382-len(ram_memory)):
    ram_memory.append(0)

# Interupts
# WR.irq(handler=wr_handler, trigger=Pin.IRQ_FALLING)
# RD.irq(handler=rd_handler, trigger=Pin.IRQ_FALLING)
# IOREQ.irq(handler=io_handler, trigger=Pin.IRQ_FALLING)

# Wait
#WAIT = Pin("GP15", Pin.OUT)
#WAIT.LOW()

# Boot up procedure
print("Memory: ", len(ram_memory))

# Read "ROM" data as binary into memory array
#with open("z80.bin", mode='rb') as file: 
#    ram_memory = bytearray(file.read())


# Clock input
Clock_Timer.init(mode=Timer.PERIODIC, callback=clock_tick, freq=1000)





    
