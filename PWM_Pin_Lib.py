"""@package PWM Pin
This class is specific to this electronic cavity experiment and for a Raspberry Pi 4.

This class helps with the management of PWM pins, their voltage, what electronic cavity they are connected to, and what their duty cycle is.
"""

import numpy as np
import RPi.GPIO as GPIO

class PWM_Pin:

    def setBoardPin(self, pinNo): self.pinNumber_BOARD = pinNo
    def setCavityPin(self, pinNo): self.pinNumber_Cavity = pinNo
    def getBoardPin(self): return self.pinNumber_BOARD
    def getCavityPin(self): return self.pinNumber_Cavity
    def setDutyCycle(self): self.pwm.changeDutyCycle(self.voltage_rPI/3.3)
    
    def __init__(self, pinBoard=np.NaN(), pinCavity=np.NaN(), dutyCycle=0, voltage_rPI=0, PWM_Freq=100):
        self.pinNumber_BOARD = pinBoard
        self.pinNumber_Cavity = pinCavity
        GPIO.setup(pinBoard, GPIO.OUT)      # Set GPIO PWM pins to output mode.
        self.pwm = GPIO.PWM(pinBoard, PWM_Freq)  # Initialize PWM on pin, 100Hz frequency
        self.voltage_rPI = voltage_rPI
        self.voltage_cavity = voltage_rPI * 5.0/3.3
        self.dutyCycle = setDutyCycle(self)
        self.maxVoltage = 3.3
        self.pwm.start(voltage_rPI/3.3*100.0)    # Start PWM with the required duty cycle to obtain the desired voltages