# rshell -p /dev/tty.usbmodem1231401
# minicom -D /dev/tty.usbmodem1231401 -b 115200

from ansi import *
from machine import Pin
from utime import sleep


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
ram_memory = []
for b in range(16384):
    ram_memory.append(0)

# LED status light
led_pin = Pin("LED", Pin.OUT)

# Write and Read signals
WR = Pin("GP0", Pin.IN)
RD = Pin("GP1", Pin.IN)

# IO Request
IOREQ = Pin("GP27", Pin.IN, Pin.PULL_UP)

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


# Output the Z80 values
def print_status(is_IO, is_reading, is_writing, this_address, this_data):
    print(top)         
    print('{:8}'.format(tick), end='') 
    print(bold + " IO: " + reset, abs(is_IO),end='')
    print(bold + " RD: " + reset, abs(is_reading), end='')
    print(bold + " WR: " + reset, abs(is_writing), end='')
    print(bold + " Address: {:#018b}".format(this_address), reset, end='')
    print(bold + " Data: {:#010b}".format(this_data), reset, end='')
    print(bold + " {:#06x}".format(this_data), reset)
    print()  
    print(clearline)


# Handle providing or writing data at an address
def romram(pin):
    global tick
    
    this_address = 0
    this_data = 0

    led_pin.toggle()

    # Check if IO
    is_IO = not (IOREQ.value())

    # When RD is low then z80 is reading
    is_reading = not (RD.value())

    # Check if is writing
    is_writing = not (WR.value())    

    # Reading from memory
    if(is_reading and not is_IO):
        this_address = get_address()
        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.OUT)
        set_pins(datavalues, ram_memory[this_address])
        this_data = ram_memory[this_address]
        tick = tick + 1 
        print_status(is_IO, is_reading, is_writing, this_address, this_data)

    # Writing to memory
    elif(is_writing and not is_IO):
        this_address = get_address()
        for data_pin in reversed(datavalues):
            data_pin.init(mode=Pin.IN)
        for data_pin in reversed(datavalues):
            this_data = (this_data << 1) + data_pin.value()
            ram_memory[this_address] = this_data
        tick = tick + 1
        print_status(is_IO, is_reading, is_writing, this_address, this_data)

    # We shouldn't respond    
    else:
        this_address = get_address()
        tick = tick + 1

    



# Clock
Clock = Pin("GP28", Pin.IN)
Clock.irq(handler=romram, trigger=Pin.IRQ_RISING)

