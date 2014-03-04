# -*- coding: utf-8 -*-

from display_pb2 import Display


class DisplayController(object):
    def __init__(self, lines):
        self.lines = lines

    def line_center(self, line_id, text):
        message = Display()
        message.style = Display.center
        message.text = text
        self.lines[line_id].send(message.SerializeToString())

    def weather_time(self, temperature, time):
        # weather = '%s%sC' % (temperature, chr(176))
        # weather = '%s%sC' % (temperature, chr(223))
        # weather = temperature + chr(223) + 'C'
        weather = "%s'C" % (temperature)
        white_spaces = ' ' * (20 - len(time) - len(weather))
        # self.line_center(4, '%s%s%s' % (weather, white_spaces, time))

        message = Display()
        message.style = Display.temp_and_time
        message.text = '%s%s%s' % (weather, white_spaces, time)
        self.lines[4].send(message.SerializeToString())
