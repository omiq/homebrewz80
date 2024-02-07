# Code based on example by NerdCave 
# Original https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/I2C%20LCD 
# Video https://www.youtube.com/watch?v=bXLgxEcT1QU

import utime
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

def message():
    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("PI Pico")
    lcd.move_to(0,1)
    lcd.putstr("LCD Control")
    utime.sleep(2)
    lcd.clear()
    utime.sleep(2)
  

while 1:   
    message()    


