# -*- coding: utf-8 -*-

import requests
import json
from time import strftime, sleep
import pylibmc
import zmq

from device_controller_pb2 import DeviceControllerMessage


class TimeAndWeatherUpdater(object):
    def __init__(self, port):
        # memcached init
        self.mc = pylibmc.Client(['127.0.0.1'], binary=True,
                                 behaviors={'tcp_nodelay': True,
                                 'ketama': True})

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
        return str(round(celsius, 1))

    def get_time(self):
        return strftime('%H:%M')

    def set_weather_time(self, weather, time):
        message = DeviceControllerMessage()
        message.from_device = DeviceControllerMessage.WeatherTimeUpdater
        message.weather = weather
        message.time = time
        self.socket.send(message.SerializeToString())

    def work(self):
        if self.mc['TNWU_running']:
            return

        temp_success = False
        while not temp_success:
            # Update only time
            time = self.get_time()
            temp = self.mc['TNWU_last_temp']
            self.set_weather_time(temp, time)

            # Update weather
            try:
                temp = self.get_temperature(self.mc['city'])
            except:
                sleep(1)
                time = self.get_time()
                self.set_weather_time(temp, time)
            else:
                temp_success = True

            time = self.get_time()
            self.set_weather_time(temp, time)

        self.mc['TNWU_last_temp'] = temp
        self.mc['TNWU_running'] = False


if __name__ == '__main__':
    mc = pylibmc.Client(['127.0.0.1'], binary=True,
                        behaviors={'tcp_nodelay': True,
                        'ketama': True})
    mc['TNWU_running'] = False
    mc['city'] = 'Moscow,ru'
    t_n_w_updater = TimeAndWeatherUpdater(mc['DC_port'])
    t_n_w_updater.work()
