"""@package PWM Pin
This class is specific to this electronic cavity experiment and for a Raspberry Pi 4.

This class helps with the management of PWM pins, their voltage, what electronic cavity they are connected to, and what their duty cycle is.
"""

import numpy as np
import RPi.GPIO as GPIO

class PWM_Pin:

    # setBoardPin sets the pin number (following BOARD pin number GPIO schema) for PWM
    def setBoardPin(self, pinNo): self.pinNumber_BOARD = pinNo
    # setCavityPin sets the cavity pin number which is connected to the PWM pin
    def setCavityPin(self, pinNo): self.pinNumber_Cavity = pinNo
    # getBoardPin gets the BOARD pin number for the PWM pin
    def getBoardPin(self): return self.pinNumber_BOARD
    # getCavityPin gets the cavity pin for a given PWM pin
    def getCavityPin(self): return self.pinNumber_Cavity
    # setDutyCycle sets the duty cycle for a desired voltage output at the cavity
    def setV_out(self, voltage):
        newDuty = voltage/5.0 * 100.0
        self.pwm.ChangeDutyCycle(newDuty)
        self.voltage_cavity = voltage
        self.voltage_rPI = voltage/5.0 * 3.3
        print("Duty cycle is now: ", newDuty)
    
    def __init__(self, pinBoard, pinCavity=0, voltage_rPI=0, PWM_Freq=200):
        GPIO.setmode(GPIO.BOARD)
        self.pinNumber_BOARD = pinBoard
        self.pinNumber_Cavity = pinCavity
        GPIO.setup(pinBoard, GPIO.OUT)           # Set GPIO PWM pins to output mode.
        self.pwm = GPIO.PWM(pinBoard, PWM_Freq)  # Initialize PWM on pin, 8kHz frequency
        self.voltage_rPI = voltage_rPI
        self.voltage_cavity = voltage_rPI/3.3 * 5.0
        self.pwm.start(0)    # Start PWM with the required duty cycle to obtain the desired voltages
        self.setV_out(self.voltage_cavity)

    def __del__(self):
        self.pwm.stop() # stop PWM