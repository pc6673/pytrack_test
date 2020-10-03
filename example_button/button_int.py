https://techtutorialsx.com/2017/10/08/esp32-micropython-external-interrupts/

import machine

pin_number = 14 
interruptCounter = 0
totalInterruptsCounter = 0
 
def callback(pin):
  global interruptCounter
  interruptCounter = interruptCounter+1
 
p25 = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)
 
p25.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)
 
while True:
 
  if interruptCounter>0:
    # The disabling and re-enabling of interrupts is done with 
    # the disable_irq and enable_irq functions of the machine module.
    state = machine.disable_irq()
    interruptCounter = interruptCounter-1
    machine.enable_irq(state)
 
    totalInterruptsCounter = totalInterruptsCounter+1
    print("Interrupt has occurred: " + str(totalInterruptsCounter))