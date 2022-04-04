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
import time

data_csv = "./Data/data.csv"
steps = 10 # steps to take in range

# Set the pin addressing in the code to the pin numbers on the board
GPIO.setmode(GPIO.BOARD)

# Create PWM Pin objects
pwm_pins = []
for pin in [12, 32, 33, 35]:
  pwm_pins.append(PWMPin.PWM_Pin(pin))
  pwm_pins[-1].setCavityPin(len(pwm_pins))

pin_table=pd.DataFrame({'Pins' : pwm_pins, 'Enable' : [True, False, False, False]})
print(pin_table)

# load old CSV file if it exists
if pth.exists(data_csv): pd.read_csv(data_csv)

pin_table['V_min'] = 0.0
pin_table['V_max'] = 0.0

for i in pin_table.index:
    if pin_table['Enable'][i]:
      pinNo = pin_table['Pins'][i]
      pin_table['V_min'][i] = 0.0
      pin_table['V_max'][i] = 5.0

print(pin_table)

# Run the test by sweeping each enabled pin
data = pd.DataFrame()

print("\nPress Ctl C to quit \n")  # Print blank line before and after message.

try:
  for i in pin_table[pin_table['Enable'] == True].index:
    for voltage in np.arange(pin_table['V_min'][i], pin_table['V_max'][i], (pin_table['V_max'][i]-pin_table['V_min'][i])/steps):
      print(voltage/5.0*3.3)
      pin_table['Pins'][i].setV_out(voltage)
      time.sleep(10)
    
except KeyboardInterrupt:
  print("Ctl C pressed - ending program")
  GPIO.cleanup()