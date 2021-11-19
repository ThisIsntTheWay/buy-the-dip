# Various auxilliary functions

import time
import socket

def getTime():
    return time.strftime("%H:%M:%S", time.localtime())

def log(msg):
    print(getTime() + " " + msg)

def hostname_resolves(hostname):
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.error:
        return False