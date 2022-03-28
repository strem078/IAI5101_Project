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
import json
import PWM_Pin_Lib as PWMPin

data_csv = "./Data/data.csv"
stepSize = 1 # percentage step in given range

# Set the pin addressing in the code to the pin numbers on the board
GPIO.setmode(GPIO.BOARD)

# Create PWM Pin objects
pwm_pins = []
for pin in [12, 32, 33, 35]:
  pwm_pins.append(PWMPin.PWM_Pin(pin))
  pwm_pins[-1].setCavityPin(len(pwm_pins))

pin_table=pd.DataFrame({'Pins_Cavity' : [1,2,3,4], 'Pins_BOARD' : pwm_pins, 'Enable' : [True, True, False, False]})
print(pin_table)

# load old CSV file if it exists
if pth.exists(data_csv): pd.read_csv(data_csv)

for i in pin_table.index:
    if pin_table['Enable'][i]:
      pinNo = pin_table['Pins_BOARD'][i]
      pin_table['V_min'][i] = 0.0
      pin_table['V_max'][i] = 5.0
    else:                          # Disabled pins have 0 to 0 as range
      pin_table['V_min'][i] = 0.0
      pin_table['V_max'][i] = 0.0

# Define a sweeping function that sweeps the range of each pin
def sweep(pinNo, range):


# Run the test by sweeping each pin recursively
data = pd.DataFrame()

try:
  for i in pin_table[pin_table.Enable].index: # Run through enabled pins
    data['Voltage_' + str(i+1)] = range(pin_table['V_min'][i], range(pin_table['V_max'][i]), stepSize*(pin_table['V_min'][i]-pin_table['V_max'][i])/100)
except KeyboardInterrupt:
  print("Ctl C pressed - ending program")

# Sweeping loop in program
print("\nPress Ctl C to quit \n")  # Print blank line before and after message.

  while True:                      # Loop until Ctl C is pressed to stop.
    for dc_1 in range(0, 101, 5):  # Loop 0 to 100 (0 to 3v3) stepping dc by 5 (165mV) each loop
      
      time.sleep(0.05)             # wait .05 seconds at current LED brightness
      print(dc)

except KeyboardInterrupt:
  

pwm.stop()                         # stop PWM
GPIO.cleanup()                     # resets GPIO ports used back to input mode