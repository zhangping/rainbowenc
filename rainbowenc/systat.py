#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time
import socket
import fcntl
import struct

def get_memusage():
    p = subprocess.Popen("free", shell=True, stdout=subprocess.PIPE).stdout
    p.readline()
    memstat = p.readline()
    return int(memstat.split()[2])/1000

def get_loadavg():
    loadavg = open("/proc/loadavg").readline()
    return loadavg

def get_cpusage():
    """
    CPU Usage, read first line of /proc/stat 
    cpu  31914006 3349 860313 44490056 4530 110394 146192 0 0
           user   nice system   idle  iowait irq   softirq
    """
    line = open("/proc/stat").readline().split()
    total0 = int(line[1])
    total0 += int(line[2])
    total0 += int(line[3])
    total0 += int(line[4])
    total0 += int(line[5])
    total0 += int(line[6])
    total0 += int(line[7])
    idle0 = int(line[4])
    time.sleep(1)
    line = open("/proc/stat").readline().split()
    total1 = int(line[1])
    total1 += int(line[2])
    total1 += int(line[3])
    total1 += int(line[4])
    total1 += int(line[5])
    total1 += int(line[6])
    total1 += int(line[7])
    idle1 = int(line[4])
    usage = 100 - ((idle1 - idle0) * 100)/(total1-total0)
    return usage

def get_uptime():
    """
    get uptime.
    """
    stat = open("/proc/stat").readlines()
    i = 0
    while 1:
        if stat[i].split()[0] == 'btime':
            btime = time.time() - int(stat[i].split()[1])
            break
        i += 1

    str_btime = str(int(btime//86400)) + ' (days) '
    str_btime += str(int((btime%86400)//3600)) + ' (hours) '
    str_btime += str(int((btime%3600)//60)) + ' (minutes)'

    return str_btime

def get_plateform():
    cpuinfo = open("/proc/cpuinfo")
    while True:
        record = cpuinfo.readline().split(":")
        if record[0] == "model name\t":
            break
        if cpuinfo == None:
            break
    return record[1]

