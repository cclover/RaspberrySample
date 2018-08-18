#-*- encoding=utf8 -*-

import RPi.GPIO as GPIO
from tm1637 import TM1637
import time

#define TM1637 pin
PIN_DIO = 14
PIN_CLK = 15

def initDisplay():
    global display
    display = TM1637(PIN_CLK, PIN_DIO, 2)
    display.Clear()


GPIO.setmode(GPIO.BCM)
initDisplay()
display.ShowInt(35)
time.sleep(5)
display.Clear()
GPIO.cleanup()

