# -*- coding: utf-8 -*-

import time
from multiprocessing import Process
import zmq

from rotary_encoder import RotaryEncoder
from switch import Switch
from hardware.device_controller_pb2 import DeviceControllerMessage, Encoder


class REException(Exception):
    pass


def RE_runner(port, name, pin_a, pin_b, button_pin):
    my_RE = RotaryEncoder(pin_a, pin_b)
    my_button = Switch(button_pin)

    p = Process(target=RE_worker, args=(port, my_RE, name, my_button))
    p.start()
    return p


def RE_worker(port, encoder, name, switcher):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect('tcp://localhost:%d' % port)
    time.sleep(1)

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
            message = DeviceControllerMessage()
            message.from_device = DeviceControllerMessage.RotaryEncoder
            message.encoder_message.name = name
            if (total_delta % 4 == 0) and (total_delta != 0):
                message.encoder_message.action = Encoder.Rotation
                message.encoder_message.snaps = total_delta / 4
                socket.send(message.SerializeToString())
                total_delta = 0
            if state != last_state:
                last_state = state
                message.encoder_message.action = Encoder.Button
                message.encoder_message.button_state = state
                socket.send(message.SerializeToString())
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
