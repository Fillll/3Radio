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

        self.r_r = read_rot()

    def bin_worker(self):
        interval = 0
        nothing_happens = 0
        while (True):
            a = self.get_delta()
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
    
    def read_rot(self):
        # a_state = self.gpio.digitalRead(self.a_pin)
        # b_state = self.gpio.digitalRead(self.b_pin)
        # r_seq = (a_state ^ b_state) | b_state << 1
        # return r_seq
        a_state = GPIO.input(self.PinA)
        b_state = GPIO.input(self.PinB)
        ret = (a_state ^ b_state) | b_state
        return ret

    def get_delta(self):
        delta = 0
        r_r = self.read_rot()
        if r_r != self.r_r:
            delta = (r_r - self.r_r)
            # if delta==3:
            #     delta = -1
            # elif delta==2:
            #     delta = int(math.copysign(delta, self.last_delta))  # same direction as previous, 2 steps
                
            self.last_delta = delta
            self.r_r = r_r

        return delta

        
if __name__ == '__main__':
    my_encoder = RotaryEnc(5, 7, 3)
    my_encoder.bin_worker()
