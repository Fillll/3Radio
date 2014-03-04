# -*- coding: utf-8 -*-

import zmq
from multiprocessing import Pipe
import pylibmc
import time
import RPi.GPIO as GPIO

from lcd.controller import DisplayController
from hardware.device_controller_pb2 import DeviceControllerMessage as DCM
from device_controller_pb2 import Encoder
from hardware.lcd.lcd_proc import LCD_runner
from hardware.rotary.rotary_encoder_proc import RE_runner


class DeviceController(object):
    '''
    DeviceController
    '''
    def __init__(self, recv_port, debug=False):
        # Debug init
        mc = pylibmc.Client(['127.0.0.1'], binary=True,
                            behaviors={'tcp_nodelay': True,
                            'ketama': True})
        try:
            self.debug = mc['debug']
        except:
            self.debug = debug
        if not self.debug:
            time.sleep(3 * 60)
            GPIO.setwarnings(False)

        # Temperature init
        mc['TNWU_last_temp'] = '-666.666'

        # ZMQ init
        self.context = zmq.Context()
        self.recv_socket = self.context.socket(zmq.SUB)
        self.recv_socket.bind('tcp://*:%d' % recv_port)
        self.recv_socket.setsockopt(zmq.SUBSCRIBE, '')

        # Display init
        recv_1, send_1 = Pipe(duplex=False)
        recv_2, send_2 = Pipe(duplex=False)
        recv_3, send_3 = Pipe(duplex=False)
        recv_4, send_4 = Pipe(duplex=False)
        lines = {1: send_1, 2: send_2, 3: send_3, 4: send_4}
        self.display = DisplayController(lines)
        self.p_lcd = LCD_runner(recv_1, recv_2, recv_3, recv_4)
        self.display.line_center(1, '3Radio')
        self.display.line_center(2, '------')
        self.display.line_center(3, '')
        self.display.line_center(4, 'Loading...')

        # Rotary encoders init
        self.state = {1: {Encoder.Rotation: 0,
                          Encoder.Button: Encoder.up},
                      2: {Encoder.Rotation: 0,
                          Encoder.Button: Encoder.up},
                      3: {Encoder.Rotation: 0,
                          Encoder.Button: Encoder.up}
                     }
        self.p_e1 = RE_runner(recv_port, 1, 8, 9, 7)
        self.p_e2 = RE_runner(recv_port, 2, 0, 2, 3)
        self.p_e3 = RE_runner(recv_port, 3, 12, 13, 14)

    def __del__(self):
        self.pe1.terminate()
        self.pe2.terminate()
        self.pe3.terminate()
        self.plcd.terminate()

    def work(self):
        while True:
            message = DCM()
            message.ParseFromString(self.recv_socket.recv())

            if message.from_device == DCM.RotaryEncoder:
                message = message.encoder_message
                encoder_id = message.name
                if message.action == Encoder.Rotation:
                    self.state[encoder_id][Encoder.Rotation] += \
                                                        message.snaps
                elif message.action == Encoder.Button:
                    self.state[encoder_id][Encoder.Button] = \
                                                        message.button_state
            elif message.from_device == DCM.WeatherTimeUpdater:
                self.display.weather_time(message.weather, message.time)
            elif message.from_device == DCM.JustPrintIt:
                self.display.line_center(message.line_number, message.text)

            if self.stop_all():
                break

    def stop_all(self):
        if ((self.state[1][Encoder.Button] == Encoder.down) and
                        (self.state[3][Encoder.Button] == Encoder.down)):
            return True


if __name__ == '__main__':
    mc = pylibmc.Client(['127.0.0.1'], binary=True,
                        behaviors={'tcp_nodelay': True,
                        'ketama': True})
    mc['DC_port'] = 6666
    device_controller = DeviceController(mc['DC_port'])
    device_controller.work()
