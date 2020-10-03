#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#


import pycom
from machine import UART
from machine import Pin
from machine import SD
from machine import RTC
import machine
import os
import time


pycom.heartbeat(False)
uart = UART(0, baudrate=115200)
os.dupterm(uart)
rtc=RTC()

# sd=SD()
# os.mounted(sd, '/sd')
# f = open('/sd/gps-record.txt', 'w')
machine.main('main.py')

##Read the button, if pressed then not in deepsleep mode and connected to your wifi
#bouton = Pin('G4',mode=Pin.IN,pull=Pin.PULL_UP)
#if bouton() == 0 or True:
#    pycom.rgbled(0xff9900) #orange
#    from network import WLAN
#   wlan = WLAN(mode=WLAN.STA)
#    nets = wlan.scan()
#    for net in nets:
#        if net.ssid == 'Iphone':
#            wlan.connect(net.ssid, auth=(net.sec, 'ly123456'), timeout=5000)
#            while not wlan.isconnected():
#                machine.idle()# Active (not a sleep mode)
#            print('Connetion WLAN/WiFi OK!')
#            rtc.ntp_sync("pool.ntp.org")
#            while not rtc.synced():
#                print("Wait to be in sync")
#                time.sleep(10)
#            print("RTC is in sync. ",rtc.now())
#            machine.main('main.py')
#            break
#
#else:
#    pycom.rgbled(0x7f0000)#red
#    #machine.deepsleep()
#    #machine.main('main.py')
