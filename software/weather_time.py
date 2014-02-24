# -*- coding: utf-8 -*-

import requests
import json
from time import strftime, sleep
import pylibmc
import zmq

from hardware.device_controller_pb2 import DeviceControllerMessage


class TimeAndWeatherUpdater(object):
    def __init__(self, port):
        # memcached init
        self.mc = pylibmc.Client(['127.0.0.1'], binary=True,
                                 behaviors={'tcp_nodelay': True,
                                 'ketama': True})


        r_c = self.mc['TNWU_reduced_connection']
        authkey = self.mc['TNWU_authkey']
        self.line_connection = r_c[0](r_c[1][0], r_c[1][1], r_c[1][2], authkey)

        # ZMQ init
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect('tcp://localhost:%d' % port)
        sleep(1)

    def get_temperature(self, city_name):
        url = 'http://api.openweathermap.org/data/2.5/weather?q=%s' % city_name
        weather_response = requests.get(url)
        weather_data = json.loads(weather_response.content)
        celsius = weather_data[u'main'][u'temp'] - 273.15
        return '%s%sC' % (str(round(celsius, 1)), chr(223))

    def get_time(self):
        return strftime('%H:%M')

    def get_line(self, temp, time):
        white_spaces = ' ' * (20 - len(time) - len(temp))
        return '%s%s%s' % (temp, white_spaces, time)

    def set_line(self, line):
        message = DeviceControllerMessage()
        message.from_device = DeviceControllerMessage.WeatherTimeUpdater
        message.weather_time = line
        self.socket.send(message.SerializeToString())

    def work(self):
        if self.mc['TNWU_running']:
            return

        temp_success = False
        while not temp_success:
            # Update only time
            time = self.get_time()
            temp = self.mc['TNWU_last_temp']
            line = self.get_line(temp, time)
            self.set_line(line)

            # Update weather
            try:
                temp = self.get_temperature(self.mc['city'])
            except:    
                sleep(1)
            else:
                temp_success = True

            time = self.get_time()
            line = self.get_line(temp, time)
            self.set_line(line)

        self.mc['TNWU_last_temp'] = temp
        self.mc['TNWU_running'] = False


if __name__ == '__main__':
    mc = pylibmc.Client(['127.0.0.1'], binary=True,
                        behaviors={'tcp_nodelay': True,
                        'ketama': True})
    t_n_w_updater = TimeAndWeatherUpdater(mc['DC_port'])
    t_n_w_updater.work()
