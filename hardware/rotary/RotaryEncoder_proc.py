# encoding:utf-8


import RotaryEncoder
import Switch
import time
from multiprocessing import Process


class REException(Exception):
    pass


def RE_runner(q, name, pin_a, pin_b, button_pin):
    my_RE = RotaryEncoder.RotaryEncoder(pin_a, pin_b)
    my_button = switch.Switch(button_pin)

    p = Process(target=RE_worker, args=(1, my_RE, name, my_button))
    p.start()

def RE_worker(q, encoder, name, switcher):
    total_delta = 0
    last_state = 0
    while True:
        delta = encoder.delta() # returns 0,1,or -1
        state = switcher.get_state()
        if (delta != 0) or (state != last_state):
            total_delta += delta
            if (total_delta % 4 == 0) and (total_delta != 0):
                q.put({'rot':total_delta/4, 'name':name})
                total_delta = 0
            if state != last_state:
                last_state = state
                q.put({'button':state, 'name':name})
            interval = 0.001
            nothing_happens = 0
        else:
            nothing_happens += 1

        # sleeping
        if nothing_happens == 1000:
            interval = 0.01
        elif nothing_happens == 100000:
            interval = 0.1
        elif nothing_happens == 10000000:
            interval = 1
        time.sleep(interval)
