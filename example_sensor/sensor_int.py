# https://randomnerdtutorials.com/micropython-interrupts-esp32-esp8266/

# import the Pin class from the machine module. 
# We also import the sleep method from the time 
# module to add a delay in our script.
from machine import Pin
from time import sleep

# Create a variable called motion that can be either
# True of False. This variable will indicate whether 
# motion was detected or not 
motion = False
# create a function called handle_interrupt
# The handle_interrupt function has an input 
# parameter (pin) in which an object of class 
# Pin will be passed when the interrupt happens 
# (it indicates which pin caused the interrupt).
# You should keep your handle_interrupt functions
# as short as possible and avoid using the print() 
# function inside.
def handle_interrupt(pin): 
# Note: as you want motionto be usable both inside 
# the function and throughout the code, it needs to 
# be declared as global. 

# Here we’re saving the pin that caused the interrupt 
# in the interrupt_pin variable. In this case, it is
# not very useful because we only have one interrupt pin. 
# However, this can be useful if we have several interrupts 
# that trigger the same interrupt handling function and we 
# want to know which GPIO caused the interrupt.
  global motion
  motion = True
  global interrupt_pin
  interrupt_pin = pin 
#  two Pin objects
led = Pin(12, Pin.OUT)
pir = Pin(14, Pin.IN)  #GPIO 14

# set an interrupt on the pir by calling the irq() method.
# handler: this is a function that will be called when an 
# interrupt is detected, in this case the handle_interrupt() function.
pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)  

while True:
  if motion:
    print('Motion detected! Interrupt caused by:', interrupt_pin)
    led.value(1)
    sleep(20)
    led.value(0)
    print('Motion stopped!')
    motion = False