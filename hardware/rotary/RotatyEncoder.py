# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class RotaryEnc(object):
    '''
    Using rotary encoder.
    '''
    
    def __init__(self, PinA, PinB, PinButton):
        self.PinA = PinA
        self.PinB = PinB
        self.PinButton = PinButton
        self.old_button = 1
        self.oldPinA = 1
        self.button_release = 0
        self.button_down = 0
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PinA, GPIO.IN)
        GPIO.setup(self.PinB, GPIO.IN)
        GPIO.setup(self.PinButton, GPIO.IN)

    def bin_worker(self):
        interval = 0
        nothing_happens = 0
        while (True):
            a = self.read_bin()
            if not a == 0:
                print a
                interval = 0
                nothing_happens = 0
            else:
                nothing_happens += 1
            
            if   nothing_happens == 1000:
                interval = 0.01
            elif nothing_happens == 100000:
                interval = 0.1
                
            time.sleep(interval)
    
    def read_bin(self):
        ret = 0
        encoderPinA = GPIO.input(self.PinA)
        encoderPinB = GPIO.input(self.PinB)
        if encoderPinA and not self.oldPinA:
            if not encoderPinB:
                ret = 1
            else:
                ret = -1
        self.oldPinA = encoderPinA
        return ret
        
if __name__ == '__main__':
    my_encoder = RotaryEnc(5, 7, 3)
    my_encoder.bin_worker()
