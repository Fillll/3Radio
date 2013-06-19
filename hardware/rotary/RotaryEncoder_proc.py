# encoding:utf-8


import RotaryEncoder
import time
from multiprocessing import Process


class REException(Exception):
    pass


def RE_runner(q, name, pin_a, pin_b, button_pin):
    my_RE = RotaryEncoder.RotaryEncoder(pin_a, pin_b)

    p = Process(target=RE_worker, args=(1, my_RE, name))
    p.start()

def RE_worker(q, encoder, name):
    total_delta = 0
    while True:
        delta = encoder.delta() # returns 0,1,or -1
        if delta!=0:
            total_delta += delta
            if (total_delta % 4 == 0) and (total_delta != 0):
                q.put({'rot':total_delta/4, 'name':name})
                total_delta = 0
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
