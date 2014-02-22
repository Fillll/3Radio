# -*- coding: utf-8 -*-

import time
from multiprocessing import Process

from rotary_encoder import RotaryEncoder
from switch import Switch


class REException(Exception):
    pass


def RE_runner(q, name, pin_a, pin_b, button_pin):
    my_RE = RotaryEncoder(pin_a, pin_b)
    my_button = Switch(button_pin)

    p = Process(target=RE_worker, args=(q, my_RE, name, my_button))
    p.start()
    return p

def RE_worker(q, encoder, name, switcher):
    nothing_happens = 0

    depth_1 = 1000
    depth_2 = depth_1 * 100
    depth_3 = depth_2 * 100

    interval = 0
    total_delta = 0
    last_state = 0
    while True:
        delta = encoder.get_delta() # returns 0,1,or -1
        state = switcher.get_state()
        if (delta != 0) or (state != last_state):
            total_delta += delta
            if (total_delta % 4 == 0) and (total_delta != 0):
                q.put({'rot': total_delta/4, 'name': name, 'dev': 're'})
                total_delta = 0
            if state != last_state:
                last_state = state
                q.put({'button': state, 'name': name, 'dev': 're'})
            interval = 0.001
            nothing_happens = 0
        else:
            nothing_happens += 1
            if nothing_happens > depth_3 * 100:
                nothing_happens = depth_3 - 1

        # sleeping
        if nothing_happens == depth_1:
            interval = 0.01
        elif nothing_happens == depth_2:
            interval = 0.1
        elif nothing_happens == depth_3:
            interval = 1
        time.sleep(interval)
