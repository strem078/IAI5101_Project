import Adafruit_MCP4725
import RPi.GPIO as GPIO
from time import sleep

MCP_translators_out_enable = [4, 5]
MCP_chan_sel = [22, 27, 18, 17]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in MCP_chan_sel:
	GPIO.setup(i, GPIO.OUT)

def prime_comms():
	for i in MCP_translators_out_enable: 
		GPIO.setup(i, GPIO.OUT)
		GPIO.output(i, 1)

# Set voltage of DAC using channel and voltage.
def setDAC(channel, voltage):
	GPIO.output(MCP_chan_sel[channel], 1)
	print(f"Setting channel {channel} to {voltage % 5000} mV") 
	dac.set_voltage(int((voltage % 5000)/5000*4095))
	GPIO.output(MCP_chan_sel[channel], 0)

prime_comms()
dac = Adafruit_MCP4725.MCP4725(address=0x61)

while True:
	for x in range(0,5000,10):
		setDAC(0, x)
		setDAC(1, 2*x)
