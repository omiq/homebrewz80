# rshell -p /dev/tty.usbmodem1231401
# minicom -D /dev/tty.usbmodem1231401 -b 115200

from ansi import *
import machine
from machine import Pin
from utime import sleep

is_IO = False
is_reading = False
is_writing = False   
this_address = 0
this_data = 0

# Get the address pins
def get_address():
    this_address = 0
    for address_pin in reversed(address):
         this_address = (this_address << 1) + address_pin.value()
    return this_address

# Set the pins to correct values
def set_pins(pins, data):
    for pin in pins:
        this_bit = data & 0x01
        if(this_bit == 1):
            pin.on()
        else:
            pin.off()
        data = (data >> 1)

  
# Clock Ticks
tick = 0

# ROM/RAM
ram_memory = [  0x3e, 0x48, # LDA H
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x65, # LDA e
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x6c, # LDA l
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x6c, # LDA l
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x6f, # LDA o
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x20, # LDA _
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x57, # LDA W
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x6f, # LDA o
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x72, # LDA r
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x6c, # LDA l
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x64, # LDA d
                0xd3, 0x00, #       OUTA 0
                0x3e, 0x21, # LDA 1
                0xd3, 0x00, #       OUTA 0
                0x76, 0x76, # HALT

]
for b in range(16384-len(ram_memory)):
    ram_memory.append(0)

# LED status light
led_pin = Pin("LED", Pin.OUT)

# Write and Read signals
WR = Pin("GP0", Pin.IN, Pin.PULL_UP)
RD = Pin("GP1", Pin.IN, Pin.PULL_UP)

# IO Request
IOREQ = Pin(27, Pin.IN, Pin.PULL_UP)

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



# Output the Z80 values
def print_status():
    global tick, is_IO, is_reading, is_writing, this_address, this_data

    print(top)         
    print('{:8}'.format(tick), end='') 
    print(bold + " IO: " + reset, abs(is_IO),end='')
    print(bold + " RD: " + reset, abs(is_reading), end='')
    print(bold + " WR: " + reset, abs(is_writing), end='')
    print(bold + " Address:" + reset + " {:#018b}".format(this_address), end='')
    print(bold + " Data:" + reset + " {:#010b}".format(this_data), end='')
    print(" {:#06x}".format(this_data), reset, end='')
    
    if this_data < 126 and this_data > 31:
        print(chr(this_data), end='')
    else:
        print("", end='')
    
    print()  
    print(clearline)


# Handle providing or writing data at an address
def romram(pin):
    global tick, is_IO, is_reading, is_writing, this_address, this_data
    
    led_pin.toggle()

    # Check if IO
    is_IO = (IOREQ.value()==0)

    # When RD is low then z80 is reading
    is_reading = (RD.value()==0)

    # Check if is writing
    is_writing = (WR.value()==0)    

    # Reading from memory
    if(is_reading and not is_IO):
        this_address = get_address()
        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.OUT)
        set_pins(datavalues, ram_memory[this_address])
        this_data = ram_memory[this_address]

        print_status()
        tick = tick + 1

    # Writing to memory
    if(is_writing and not is_IO):
        this_address = get_address()
        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.IN)
        for data_pin in reversed(datavalues):
            this_data = (this_data << 1) + data_pin.value()
            ram_memory[this_address] = this_data

        print_status()
        tick = tick + 1


    if(is_IO):

        this_address = get_address()

        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.OUT)
        set_pins(datavalues, ram_memory[this_address])
        this_data = ram_memory[this_address]

        print_status()
        tick = tick + 1


# Clock input
Clock = Pin("GP28", Pin.IN)
Clock.irq(handler=romram, trigger=Pin.IRQ_RISING)

# Boot
print(clear)
print()
machine.freq(270000000)
print(machine.freq())
print("Boot",end='')

# Read "ROM" data as binary into memory array
#with open("z80.bin", mode='rb') as file: 
#    ram_memory = bytearray(file.read())