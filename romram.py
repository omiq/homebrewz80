from machine import Pin
from utime import sleep

def m_pin_handler(p):
    if MREQ.value():
        led_pin.value(0)
    else:
        led_pin.value(1)
    sleep(0.1) # wait for 0.1 second
    
def io_pin_handler(p):
    if IOREQ.value():
        print("IO: OFF")
    else:
        print("IO: ON")
    sleep(0.1) # wait for 0.1 second

def w_pin_handler(p):
    if MREQ.value():
        print("W: OFF")
    else:
        print("W: ON")
    sleep(0.1) # wait for 0.1 second

def r_pin_handler(p):
    if MREQ.value():
        print("R: OFF")
    else:
        print("R: ON")
    sleep(0.1) # wait for 0.1 second



# LED status light
led_pin = Pin("LED", Pin.OUT)

# Write and Read signals
WR = Pin("GP0", Pin.IN)
WR.irq(handler=w_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

RD = Pin("GP1", Pin.IN)
RD.irq(handler=r_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# IO Request
IOREQ = Pin("GP27", Pin.IN)
IOREQ.irq(handler=io_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# Memory Request
MREQ = Pin("GP28", Pin.IN)
MREQ.irq(handler=m_pin_handler,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# Address Pins
print("Address pins 1-14")
A3 = Pin("GP2", Pin.IN)
A4 = Pin("GP3", Pin.IN)
A5 = Pin("GP4", Pin.IN)
A6 = Pin("GP5", Pin.IN)
A7 = Pin("GP6", Pin.IN)
A8 = Pin("GP7", Pin.IN)
A9 = Pin("GP8", Pin.IN)
A10 = Pin("GP9", Pin.IN)
A11 = Pin("GP10", Pin.IN)
A12 = Pin("GP11", Pin.IN)
A13 = Pin("GP12", Pin.IN)
A14 = Pin("GP13", Pin.IN)
A15 = Pin("GP14", Pin.IN)
A16 = Pin("GP15", Pin.IN)

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
print("Boot")
while True:
    try:
        READ_ENABLE = RD.value()
    except KeyboardInterrupt:
        break
led_pin.off()
