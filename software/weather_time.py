# -*- coding: utf-8 -*-

import requests
import json
from time import strftime, sleep
from multiprocessing import Process


def get_temperature(city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=%s' % city_name
    weather_response = requests.get(url)
    weather_data = json.loads(weather_response.content)
    celsius = weather_data[u'main'][u'temp'] - 273.15
    return '%s%sC' % (str(round(celsius, 1)), chr(223))


def get_weather_time(line, city_name):
    temperature = get_temperature(city_name)
    time = strftime('%H:%M')
    white_spaces = ' ' * (20 - len(time) - len(temperature))
    return '%s%s%s' % (temperature, white_spaces, time)


def set_weather_time(line, city_name):
    line.put({'text': get_weather_time(line, city_name), 'style': 'center'})


def weather_time_worker(line, city_name):
    while True:
        try:
            set_weather_time(line, city_name)
            sleep(59)
        except:
            sleep(1)


def weather_time_runner(line, city_name):
    p = Process(target=weather_time_worker, args=(line, city_name))
    p.start()
    return p
