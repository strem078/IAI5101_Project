from pickle import TRUE
import numpy as np
import pandas as pd
import random
from datetime import datetime
import pytz
tz = pytz.timezone("US/Eastern")

from rpi_hardware_pwm import HardwarePWM
import glob
import smbus
from MCP342x import MCP342x
from time import sleep

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

def foo(v1,v2):
    pwm1.change_duty_cycle(100.0*v1/3300)
    pwm2.change_duty_cycle(100.0*v2/3300)
    sleep(.3)
    r = MCP342x.convert_and_read_many(adcs, samples=10)
    sleep(.3)
    px = np.mean(r[0])
    py = np.mean(r[1])
    s1 = (px-py)/(px+py)
    
    pwm1.change_duty_cycle(100.0*v1/3300)
    new_v2_duty = 100.0*v2/3300-15
    if(new_v2_duty < 0):
        if(100.0*v1/3300 - 15 < 0): pwm1.change_duty_cycle(0)
        else: pwm1.change_duty_cycle(100.0*v1/3300 - 15)
        pwm2.change_duty_cycle(100.0 + new_v2_duty)
    else: pwm2.change_duty_cycle(100.0*v2/3300 - 15)

    sleep(.3)
    r = MCP342x.convert_and_read_many(adcs, samples=10)
    sleep(.3)
    px_prev = np.mean(r[0])
    py_prev = np.mean(r[1])
    s1_prev = (px_prev-py_prev)/(px_prev+py_prev)

    dS1 = s1 - s1_prev
    # py_min_px = py - px - 0.7
    # bound_px_py = 645492*py_min_px**4 - 284017*py_min_px**3 + 47317*py_min_px**2 - 3536.5*py_min_px + 100
    # bound_s1 = 762078951.4*(dS1-.02)**4 - 54869684.5*(dS1-.02)**3 + 1543210*(dS1-.02)**2 - 20000*(dS1-.02) + 100
    # fit = bound_px_py + bound_s1

    #fit = int(not 0.7 < (py - px) < 0.92)*0.5 + (not 0.02 < dS1 < 0.056)*0.5
    #fit = abs(py/2-px)
    fit = 1/2**((px/0.940)+(py/1.65)+(dS1/0.047)-3)
    print(f"Testing {v1}, {v2}: {px}, {py},{dS1} => {fit}")
    
    return fit

def fitness(v1,v2):
    ans = foo(v1,v2)

    if ans == 0:
        return 99999
    else:
        return abs(1/ans)

pwm1 = HardwarePWM(pwm_channel=0, hz=500)
pwm2 = HardwarePWM(pwm_channel=1, hz=500)
bus = get_smbus()

# Create objects for each signal to be sampled
addr68_ch0 = MCP342x(bus, 0x68, channel=0, resolution=14, gain=1)
addr68_ch1 = MCP342x(bus, 0x68, channel=1, resolution=14, gain=1)
adcs = [addr68_ch0, addr68_ch1]

pwm1.start(0)
pwm2.start(0)

#generate solutions
solutions = []
for s in range(0,20):
    solutions.append( (random.uniform(0,3300), random.uniform(0,3300)) )

#genetic algorithm
#Generate generation 1
for i in range(10):

    rankedsolutions = []
    for s in solutions:
        rankedsolutions.append( (fitness(s[0],s[1]), s) )
    rankedsolutions.sort()
    rankedsolutions.reverse()

    print(f"=== Gen {i} best solutions ===")
    print(rankedsolutions[0])

    if rankedsolutions[0][0] > 1E12:
        break
    
    bestsolutions = rankedsolutions[:5]


    elements_0 = []
    elements_1 = []
    for s in bestsolutions:
        elements_0.append(s[1][0])
        elements_1.append(s[1][1])


    newGen = []
    for _ in range(10):
        e1 = random.choice(elements_0) * random.uniform(0.99, 1.01)
        e2 = random.choice(elements_1) * random.uniform(0.99, 1.01)

        newGen.append((e1,e2))

    solutions = newGen