#-*- encoding=utf8 -*-
'''
@author: cheng chao
@contact: chengchao128@gmail.com
@file: trafficMain.py
@time: 2018-8-18
@desc:
'''

import RPi.GPIO as GPIO
import sys
import time
import threading
import signal

from timer import LoopTimer
from tm1637 import TM1637

#define LED PIN
PIN_LIGHT_RED = 25
PIN_LIGHT_BLUE = 8
PIN_LIGHT_GREEN = 7

#define buzzer PIN
PIN_BUZZER = 24

#define TM1637 pin
PIN_DIO = 14
PIN_CLK = 15

#LED Status
LED_STATUS_OFF = 0
LED_STATUS_ON = 1
LED_STATUS_BLINK = 2

#Traffic Light time
TIME_LIGHT_RED = 10
TIME_LIGHT_BLUE = 3
TIME_LIGHT_GREEN = 10
TIME_BLINK_GREEN = 3
TIME_INTERVAL = 1

#light list
light_list = [ PIN_LIGHT_RED, PIN_LIGHT_BLUE, PIN_LIGHT_GREEN ] 

#remain timer
reaminTime = 0



def initLED():
    print "Init LED!!"
    GPIO.setup(light_list, GPIO.OUT)

def initBuzzer():
    print "Init Buzzer"
    GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.HIGH)

def initDisplay():
    global display
    display = TM1637(PIN_CLK, PIN_DIO, 2)
    display.Clear()


def init():
    print "Init Traffic!!"
    GPIO.setmode(GPIO.BCM)
    initLED()
    initBuzzer()
    initDisplay()

def destory(signum, frame):
    print "Destory Traffic!!"
    global display
    display.cleanup()
    GPIO.cleanup()
    exit()

def switchLight(light, status):

    if not light in light_list:
        return
    if status == LED_STATUS_OFF:
        print "LIGHT OFF {0}".format(light)
        GPIO.output(light, GPIO.LOW)
    elif status == LED_STATUS_ON:
        print "LIGHT ON {0}".format(light)
        GPIO.output(light, GPIO.HIGH)

def blinkLight(light):

    print "blinkLight"
    switchLight(light, LED_STATUS_OFF)
    time.sleep(0.3)
    switchLight(light, LED_STATUS_ON)
    time.sleep(0.3)
    switchLight(light, LED_STATUS_OFF)
    time.sleep(0.3)
    switchLight(light, LED_STATUS_ON)

def beepBuzzer(trig):
    print "beepBuzzer"
    GPIO.output(trig,GPIO.LOW) 
    time.sleep(0.3)
    GPIO.output(trig,GPIO.HIGH) 
    time.sleep(0.3)
    GPIO.output(trig,GPIO.LOW) 
    time.sleep(0.3)
    GPIO.output(trig,GPIO.HIGH) 

def showTime(sec):
    global display
    display.ShowInt(sec)


def redInterval():

    global reaminTime
    reaminTime = reaminTime - 1
    print "Read remain: {0}s".format(reaminTime)
    showTime(reaminTime)

def redTraffic():

    #red timer
    global reaminTime
    reaminTime = TIME_LIGHT_RED
    lightTimer = LoopTimer(TIME_LIGHT_RED, TIME_INTERVAL, redInterval, greenTraffic)
    
    #light red
    switchLight(PIN_LIGHT_GREEN, LED_STATUS_OFF)
    switchLight(PIN_LIGHT_RED, LED_STATUS_ON)
    switchLight(PIN_LIGHT_BLUE, LED_STATUS_OFF)
    
    #show time
    global display
    display.ShowInt(reaminTime)

    # start time
    print "Light on red {0}s".format(reaminTime)
    lightTimer.start()



def blueInterval():

    global reaminTime
    reaminTime = reaminTime - 1
    print "Blue remain: {0}s".format(reaminTime)
    showTime(reaminTime)

def blueTraffic():

    #blue timer
    global reaminTime
    reaminTime = TIME_LIGHT_BLUE
    lightTimer = LoopTimer(TIME_LIGHT_BLUE, TIME_INTERVAL, blueInterval, redTraffic)

    #light blue
    switchLight(PIN_LIGHT_GREEN, LED_STATUS_OFF)
    switchLight(PIN_LIGHT_RED, LED_STATUS_OFF)
    switchLight(PIN_LIGHT_BLUE, LED_STATUS_ON)

    #show time
    global display
    display.ShowInt(reaminTime)

    # start time
    print "Light on blue {0}s".format(reaminTime)
    lightTimer.start()



def greenInterval():

    global reaminTime
    reaminTime = reaminTime - 1
    print "Green remain: {0}s".format(reaminTime)
    showTime(reaminTime)
    if reaminTime <= TIME_BLINK_GREEN:
       t1 = threading.Thread(target=blinkLight,args=(PIN_LIGHT_GREEN,))
       t2 =  threading.Thread(target=beepBuzzer,args=(PIN_BUZZER,))
       t1.start()
       t2.start()

def greenTraffic():

    #green timer
    global reaminTime
    reaminTime = TIME_LIGHT_GREEN
    lightTimer = LoopTimer(TIME_LIGHT_GREEN, TIME_INTERVAL, greenInterval, blueTraffic)
    
    #light green
    switchLight(PIN_LIGHT_GREEN, LED_STATUS_ON)
    switchLight(PIN_LIGHT_RED, LED_STATUS_OFF)
    switchLight(PIN_LIGHT_BLUE, LED_STATUS_OFF)
    
    #show time
    global display
    display.ShowInt(reaminTime)

    # start time
    print "Light on green {0}s".format(reaminTime)
    lightTimer.start()

def registerExit():
    signal.signal(signal.SIGINT, destory)
    signal.signal(signal.SIGTERM, destory)


#main funciton
init()
registerExit()
print "Start traffic!!"
print "Press 'Ctrl+C' to exit..."
greenTraffic()
