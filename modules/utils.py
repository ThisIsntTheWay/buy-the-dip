# Various auxilliary functions

import time

def getTime():
    return time.strftime("%H:%M:%S", time.localtime())

def log(msg):
    print(getTime() + " " + msg)