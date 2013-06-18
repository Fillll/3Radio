# encoding:utf-8


from hardware.rotary.RotaryEncoder import RotaryEncoder
#import gaugette.switch ## TODO: switch
import math
import time

A_PIN  = 7
B_PIN  = 9
SW_PIN = 8

encoder = gaugette.rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
switch = gaugette.switch.Switch(SW_PIN)

last_state = None
last_switch_state = None
last_delta = 0
last_sequence = encoder.rotation_sequence()
last_heading = 0

# NOTE: the library includes individual calls to get
# the rotation_state, rotation_sequence and delta values.  
# However this demo only reads the rotation_state and locally
# derives the rotation_sequence and delta.  This ensures that
# the derived values are based on the same two input bits A and B.
# If we used the library calls, there is a very real chance that
# the inputs would change while we were sampling, giving us 
# inconsistent values in the output table.

interval = 0
nothing_happens = 0 

total_delta = 0

while True:

    state = encoder.rotation_state()
    switch_state = switch.get_state()

    if (state != last_state or switch_state != last_switch_state):
        last_switch_state = switch_state
        last_state = state

        # extract individual signal bits for A and B
        a_state = state & 0x01
        b_state = (state & 0x02) >> 1

        # compute sequence number:
        # This is the same as the value returned by encoder.rotation_sequence()
        sequence = (a_state ^ b_state) | b_state << 1

        # compute delta:
        # This is the same as the value returned by encoder.get_delta()
        delta = (sequence - last_sequence) % 4
        if delta == 3:
            delta = -1
        elif delta==2:
            # this is an attempt to make sense out of a missed step:
            # assume that we have moved two steps in the same direction
            # that we were previously moving.
            delta = int(math.copysign(delta, last_delta))
        last_delta = delta
        last_sequence = sequence


        nothing_happens += 1

        total_delta += delta

        if (total_delta % 4 == 0) and (total_delta != 0):
            print total_delta/4
            total_delta = 0
        interval = 0.001
        nothing_happens = 0
    else:
        nothing_happens += 1
    
    if nothing_happens == 1000:
        interval = 0.01
    elif nothing_happens == 100000:
        interval = 0.1
    elif nothing_happens == 10000000:
        interval = 1

    time.sleep(interval)
