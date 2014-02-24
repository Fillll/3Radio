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
