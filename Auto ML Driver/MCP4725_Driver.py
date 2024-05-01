import Adafruit_MCP4725
import RPi.GPIO as GPIO
import time
import glob
import logging
import smbus
from MCP342x import MCP342x
import numpy as np

def get_smbus():
    candidates = []
    prefix = '/dev/i2c-'
    for bus in glob.glob(prefix + '*'):
        try:
            n = int(bus.replace(prefix, ''))
            candidates.append(n)
        except:
            pass
    
    return smbus.SMBus(1)
    if len(candidates) == 1:
        return smbus.SMBus(candidates[0])
    elif len(candidates) == 0:
        raise Exception("Could not find an I2C bus")
    else:
        raise Exception("Multiple I2C busses found")

class Auto_Ml:

	def __init__(self):
		self.MCP_translators_out_enable = [4, 5]
		self.MCP_chan_sel = [22, 17, 27, 18]

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		
		# Set MCP selectors to outputs. Deselect all.
		for i in self.MCP_chan_sel:
			GPIO.setup(i, GPIO.OUT)
			GPIO.output(i, 0)
		
		# Set translators output enable to high.
		for i in self.MCP_translators_out_enable: 
			GPIO.setup(i, GPIO.OUT)
			GPIO.output(i, 1)
		
		self.dac = Adafruit_MCP4725.MCP4725(address=0x61)
		
		#logging.basicConfig(level='DEBUG')
		#logger = logging.getLogger(__name__)
		bus = get_smbus()
		
		# Create ADC objects for px and py readings
		self.adc_px = MCP342x(bus, 0x68, channel=1, resolution=14, gain=1)
		self.adc_py = MCP342x(bus, 0x68, channel=0, resolution=14, gain=1)
		self.adcs = [self.adc_px, self.adc_py]

	# Set voltage of DAC on specific channel.
	def setDAC(self, channel, voltage):
		GPIO.output(self.MCP_chan_sel[channel], 1)
		self.dac.set_voltage(int((voltage % 5001)/5000*4095))
		GPIO.output(self.MCP_chan_sel[channel], 0)
		
	def resetDAC(self, channel, voltage):
		setDAC(channel, 0)
	
	def readADC(self, samples=3, delay=0):
		px, py = MCP342x.convert_and_read_many(self.adcs, samples=samples)
		time.sleep(delay)
		px = np.mean(px)
		py = np.mean(py)
		return px, py
		
