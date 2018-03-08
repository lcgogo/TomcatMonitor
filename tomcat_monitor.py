#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib2
import socket
import time
import os
import re

URL = 'http://localhost:8080'
SOCKET_TIMEOUT = 10
RESTART_WAIT = 5
#LOG_FILE = "/var/log/tomcat/catalina.out"
LOG_FILE = "/var/log/tomcat/catalina.2018-03-08.log"
#ERROR_KEYWORD = "OutOfMemory"
ERROR_KEYWORD = "error"

# def return code
# 0 is normal, others are error.

def StatusCheck():
    tomcatStatus = os.system("systemctl status tomcat")
    #print(tomcatStatus)
    tomcatStatus = tomcatStatus >> 8 #get the 'echo #?' of 'systemctl status tomcat'
    if tomcatStatus != 0:
        return 1
    else:
        return 0

def LogCheck():
    with open(LOG_FILE, 'r') as f:
        f.seek(-10000,2)
        for row in f.readlines():
            if re.search(ERROR_KEYWORD, row, re.IGNORECASE):
                return 1
        return 0

def RequestTest():
    socket.setdefaulttimeout(SOCKET_TIMEOUT)
    try:
        req = urllib2.urlopen(URL)
    except urllib2.URLError,err1:
        print(err1.reason)
        return 1
    except socket.error,err2:
        print(err2)
        return 1
    else:
        return 0

def RestartTomcat():
    os.system("systemctl restart tomcat")
    print("Tomcat restarted.")
    time.sleep(RESTART_WAIT)
    if StatusCheck() != 0:
        print("Tomcat restart is failed, need manual check with 'systemctl status tomcat'.")
        return 1
    else:
        print("Tomcat restart is OK.")
        return 0 

def main():
    resultStatusCheck = StatusCheck()
    if resultStatusCheck != 0: print("Tomcat status is inactive.")

    resultLogCheck = LogCheck()
    if resultLogCheck != 0: print('Find error "%s" in tomcat log "%s".' % (ERROR_KEYWORD, LOG_FILE))

    if resultStatusCheck == 0 and resultLogCheck == 0:
        resultRequestTest = RequestTest()
        if resultRequestTest != 0: print("Request http://localhost:8080 failed.")
    else:
        resultRequestTest = 0

    if resultStatusCheck != 0 or resultLogCheck !=0 or resultRequestTest !=0:        
        print("Need restart tomcat.")
        RestartTomcat()

if __name__ == "__main__": main()
