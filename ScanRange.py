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
import PWM_Pin_Lib as PWMPin
import time
import datetime

# The ADC code was written by Steve Marple and is 
# used under the MIT Licence
import glob
import smbus
from MCP342x import MCP342x

data_csv = "./Data/data.csv"
steps = 10 # steps to take in range

# Set the ADC up
def get_smbus():
    candidates = []
    prefix = '/dev/i2c-'
    for bus in glob.glob(prefix + '*'):
        try:
            n = int(bus.replace(prefix, ''))
            candidates.append(n)
        except:
            pass
        
    if len(candidates) == 1:
        return smbus.SMBus(candidates[0])
    elif len(candidates) == 0:
        raise Exception("Could not find an I2C bus")
    else:
        raise Exception("Multiple I2C busses found")

bus = get_smbus()

# Set the ADC channels
ADC_Px_in = MCP342x(bus, 0x68, channel=0, resolution=14, gain=1)
ADC_Py_in = MCP342x(bus, 0x68, channel=1, resolution=14, gain=1)
adcs = [ADC_Px_in, ADC_Py_in]

# Create PWM Pin objects
pwm_pins = []
for pin in [12, 32, 33, 35]:
  pwm_pins.append(PWMPin.PWM_Pin(pin))
  pwm_pins[-1].setCavityPin(len(pwm_pins))

# Set starting voltages
start_voltages_cavity = [0, 0, 0, 0]
for pin in range(0,len(pwm_pins)): pwm_pins[pin].setV_out(start_voltages_cavity[pin])

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
data = pd.DataFrame({'Voltage_0':[], 'Voltage_1':[],'Voltage_2':[],'Voltage_3':[],'P_x':[],'P_y':[],'S1':[]})

print("\nPress Ctl C to quit \n")  # Print blank line before and after message.

# Function to get the power readings from the cavity
def read_powers(tolerance, samples, max_conversions=0, delay=0):
  i=0 # Conversions counter
  while i < max_conversions and max_conversions != 0:
    time.sleep(delay)
    p_x, p_y = MCP342x.convert_and_read_many(adcs, samples=samples)
    if np.abs(np.max(p_x) - np.min(p_x)) < 2.0*tolerance and np.abs(np.max(p_y) - np.min(p_y)) < 2.0*tolerance:
      return [np.average(p_x), np.average(p_y)]
    i = i+1
  
  return [np.nan(), np.nan()] # If we reached max conversions with no success

def add_data(p_x, p_y):
  V_0 = pin_table['Pins'][0].getCavityVoltage()
  V_1 = pin_table['Pins'][1].getCavityVoltage()
  V_2 = pin_table['Pins'][2].getCavityVoltage()
  V_3 = pin_table['Pins'][3].getCavityVoltage()
  S1 = (p_x-p_y)/(p_x+p_y)
  row = {'Voltage_0':[V_0], 'Voltage_1':[V_1], 'Voltage_2':[V_2], 'Voltage_3':[V_3], 'P_x':[p_x], 'P_y':[p_y], 'S1':[S1]}
  newRow = pd.DataFrame(row)
  return newRow

def increment_voltage(onPins, ptr):
  V_max = pin_table['V_max'][onPins[ptr]]
  V_min = pin_table['V_min'][onPins[ptr]]
  currPin = pin_table['Pins'][onPins[ptr]]
  if currPin.getCavityVoltage() >= V_max:
    if ptr == 0: # Sweep end condition
      return np.nan()
    else:
      increment_voltage(onPins, ptr-1)
      currPin.setV_out()
  else:
    currPin.incrementV_out((V_max-V_min)/steps)

try:
  onPins = pin_table[pin_table['Enable']].index
  ptr = len(onPins)
  while True:
    # Increment the output voltage
    increment_voltage(onPins, ptr)
    # Read the ADC input
    p_x, p_y = read_powers(0.01, 20, 100)
    if p_x == np.nan(): break; # We've reached the end of the sweep range
    data = pd.concat([data, add_data(p_x, p_y)]) # Append data point
    
  # Dump to csv file for post processing
  data.to_csv('./Data/CavityData_' + datetime.now() + '.csv')

except KeyboardInterrupt:
  print("Ctl C pressed - ending program")