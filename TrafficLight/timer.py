# -*- coding: utf-8 -*-
'''
@author: cheng chao
@contact: chengchao128@gmail.com
@file: timer.py
@time: 2018-8-18
@desc:
'''

from threading import Timer

class LoopTimer( object ):

    def __init__( self, druation, interval, interval_callback, stop_callback):

        self.__timer = None
        self.__druation = druation
        self.__interval = interval
        self.__interval_callback = interval_callback
        self.__stop_callback = stop_callback

    def start( self ):
        self.__timer = Timer( self.__interval, self.exec_callback )
        self.__timer.start()

    def cancel( self ):
        self.__timer.cancel() 
        self.__timer = None

    def exec_callback( self):
        
        self.__druation -= 1
        if self.__druation > 0:
            self.__interval_callback()
            self.start()
        else:
            self.cancel()
            self.__stop_callback()


# test method
# count = 10
# def callback():
#     global count
#     count -= 1
#     print "Count is: {0}".format(count)

# def callback2():
#     global count
#     count -= 1
#     print "Stop Timer. Count: {0}".format(count)
#     exit

# print "Start Timer. Count: {0}".format(count)
# tmr = LoopTimer(10, 1, callback, callback2)
# tmr.start()
