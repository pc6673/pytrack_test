# https://techtutorialsx.com/2017/10/08/esp32-micropython-external-interrupts/

import machine

interruptCounter = 0
totalInterruptsCounter = 0
 
def pin_handler(pin):
  global interruptCounter
  interruptCounter = interruptCounter+1
 
p14 = machine.Pin('P14', machine.Pin.IN, machine.Pin.PULL_UP)
 
p14.callback(trigger=machine.Pin.IRQ_FALLING, handler=pin_handler)
 
while True:
 
  if interruptCounter>0:
    # The disabling and re-enabling of interrupts is done with 
    # the disable_irq and enable_irq functions of the machine module.
    state = machine.disable_irq()
    interruptCounter = interruptCounter-1
    machine.enable_irq(state)
 
    totalInterruptsCounter = totalInterruptsCounter+1
    print("Interrupt has occurred: " + str(totalInterruptsCounter))