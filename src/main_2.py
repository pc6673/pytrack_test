#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
# ways to sleep pytrack can be found at https://forum.pycom.io/topic/3735/ways-to-sleep-pytrack/2
##pytrack.go_to_sleep()
#User interrupt: Disconnect and reconnect power to device
#Deep sleep (resets board upon wake up and runs boot.py and main.py)
#Initialize sleep duration using pytrack.setup_sleep([sec])
#Use: deep sleep for low power consumption
#Built-in interrupt: accelerometer (e.g. acc.enable_activity_interrupt(2000, 400, 100, handler=my_activity_handler)) or input on PIC - RC1, Pin#6 on External IO Header


# use the pytrack module with the lopy4 pycom to record the position and transmit it over Lorawan
# not in deepsleep

from network import LoRa
import socket
import binascii
import struct
import time
import config
import pycom
import utime
from machine import Pin
from L76GNSS import L76GNSS
from pytrack import Pytrack



def convert_payload(lat, lon, alt, hdop):
    """
        Converts to the format used by ttnmapper.org
    """
    payload = []
    latb = int(((lat + 90) / 180) * 0xFFFFFF)
    lonb = int(((lon + 180) / 360) * 0xFFFFFF)
    altb = int(round(float(alt), 0))
    hdopb = int(float(hdop) * 10)

    payload.append(((latb >> 16) & 0xFF))
    payload.append(((latb >> 8) & 0xFF))
    payload.append((latb & 0xFF))
    payload.append(((lonb >> 16) & 0xFF))
    payload.append(((lonb >> 8) & 0xFF))
    payload.append((lonb & 0xFF))
    payload.append(((altb  >> 8) & 0xFF))
    payload.append((altb & 0xFF))
    payload.append(hdopb & 0xFF)
    return payload

  
# initialize Lora in Lorawan
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('260012F1'))[0] #lopy1
nwk_swkey = binascii.unhexlify('719255FE369E23D4D46FEA19616DD0E7')
app_swkey = binascii.unhexlify('40E4A604E0463C2CF3AE6DABF340C708')

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# wait until the module has joined the network
while not lora.has_joined():
    pycom.rgbled(0x7f7f00) #yellow
    time.sleep(2.5)
    print('Not joined yet...')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket blocking
s.setblocking(True)

# starting the gps
py = Pytrack()
gps = L76GNSS(py, timeout=30)
time.sleep(1)
coord = gps.coordinates()
time.sleep(1)

# IRQ of button
interruptCounter = 0
totalInterruptsCounter = 0  
  
def pin14_handler(pin):
  global interruptCounter
  interruptCounter = interruptCounter+1
  pycom.rgbled(0x007f00) #GREEN
  # s.send(struct.pack("<i",  int(coord[0]*100000))+struct.pack("<i",  int(coord[1]*100000))+struct.pack("<H",  int(utime.time())))
  s.send("Iam here")
  time.sleep(1)# delay to ensure message sent before going to sleep
  lora.nvram_save() #nvram 
  
pin14 = machine.Pin('P14', machine.Pin.IN, machine.Pin.PULL_UP)
 
pin14.callback(trigger=machine.Pin.IRQ_FALLING, handler=pin14_handler)

# main lopp
while(True):

    coord = gps.coordinates()
    print("{} - {}".format(coord, rtc.now()))
    time.sleep(5)   # maybe no need to print coord frequently
    # button press trigger detect
    # keep this interruptCounter because  hope to know there was one pin button interrupt just generated
    if interruptCounter>0:
      # The disabling and re-enabling of interrupts is done with 
      # the disable_irq and enable_irq functions of the machine module.
      state = machine.disable_irq()
      interruptCounter = interruptCounter-1
      machine.enable_irq(state)
      print("button interrupt complete and data sent")
      totalInterruptsCounter = totalInterruptsCounter+1
      print("Total button interrupt times is: " + str(totalInterruptsCounter))
      print(utime.localtime())#utime
      print(utime.time())#utime


    #sleep
    #print("sleep")
    #py.setup_sleep(600 - time.time())#Initialize sleep duration for 10mins
    #py.go_to_sleep(gps=True)#use Deep sleep (resets board upon wake up and runs boot.py and main.py),keep gps powered during deepsleep of the pytrack module
