"""@package ScanRange
This code is made to be run on a Raspberry Pi 4.

This code sweeps the range of inputs to an electronic cavity in a optical circuit. The ultimate goal of this code is to obtain mode locking in a small and affordable form factor.

The effect of sweeping these values is captured at the output of the circuit, where 90% (in the experimental circuit) of the light in the circuit is split into an x- and a y-polarized output, read by photosensors (px and py) and logged into a CSV file along with the output voltages that lead to the state of the circuit.
"""

# This code was written for use on a Raspberry Pi 4
import RPi.GPIO as GPIO
import pandas as pd
import os.path as pth
import numpy as np
# import time
# import multiprocessing

data_csv = "./Data/data.csv"

# Set the pin addressing in the code to the pin numbers on the board
GPIO.setmode(GPIO.BOARD)

pwm_pins = [12, 32, 33, 35]
pin_table=pd.DataFrame({'Pins_Cavity' : [1,2,3,4], 'Pins_BOARD' : pwm_pins, 'Enable' : [True, True, False, False]})
print(pin_table)

# load old CSV file if it exists
if pth.exists(data_csv): pd.read_csv(data_csv)

for i in range(0,len(pin_table['Enable'])):
    if pin_table['Enable'][i]:
      pinNo = pin_table['Pins_BOARD'][i]
      GPIO.setup(pinNo, GPIO.OUT)  # Set GPIO PWM pins to output mode.
      pwm = GPIO.PWM(pinNo, 100)   # Initialize PWM on pwmPins, 100Hz frequency

# Sweeping loop in program
print("\nPress Ctl C to quit \n")  # Print blank line before and after message.
dc_1=0                               # set dc variable to 0 for 0%
pwm.start(dc)                      # Start PWM with 0% duty cycle (0V)

try:
  while True:                      # Loop until Ctl C is pressed to stop.
    for dc_1 in range(0, 101, 5):    # Loop 0 to 100 (0 to 3v3) stepping dc by 5 (165mV) each loop
      pwm.ChangeDutyCycle(dc)
      time.sleep(0.05)             # wait .05 seconds at current LED brightness
      print(dc)

except KeyboardInterrupt:
  print("Ctl C pressed - ending program")

pwm.stop()                         # stop PWM
GPIO.cleanup()                     # resets GPIO ports used back to input mode