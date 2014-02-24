# encoding:utf-8

import time
from multiprocessing import Process

from lcd import LCD20x4
from hardware.lcd.display_pb2 import Display


class LCDException(Exception):
    pass


def LCD_runner(q1, q2, q3, q4):
    '''
    Run process for all 4 lines
    '''
    my_lcd = LCD20x4(26, 24, 22, 18, 16, 12, 10)

    p = Process(target=LCD_worker, args=(q1, q2, q3, q4, my_lcd))
    p.start()
    return p


def get_text_from(q, counter):
    if not q.poll():
        return None, counter

    message = None
    while q.poll():
        message = Display()
        message.ParseFromString(q.recv())
        
    return message, 0


def change_text_and_style(message, text, style):
    if message is None:
        return text, style
    else:
        return str(message.text), message.style


def print_line(text, lcd, line_style, counter, white):
    if len(text) <= lcd.LCD_WIDTH:
        to_print = text
    else:
        text = '%s%s%s' % (white, text, white)
        if counter == len(text) - lcd.LCD_WIDTH + 1:
            counter = 1
        to_print = text[counter:]
        counter += 1

    getattr(lcd, line_style)(to_print)

    return counter


def LCD_worker(q1, q2, q3, q4, lcd, white=5, delay=0.5):
    """
    """
    white = ' ' * white  # Whiting length
    counter_1 = counter_2 = counter_3 = counter_4 = 0
    text_1 = text_2 = text_3 = text_4 = '0'
    style_1 = style_2 = style_3 = style_4 = Display.center

    while True:
        new_message_1, counter_1 = get_text_from(q1, counter_1)
        new_message_2, counter_2 = get_text_from(q2, counter_2)
        new_message_3, counter_3 = get_text_from(q3, counter_3)
        new_message_4, counter_4 = get_text_from(q4, counter_4)

        # if isinstance(new_message_4, dict):
        #     if 'stop' in new_message_4:
        #         break

        text_1, style_1 = change_text_and_style(new_message_1, text_1, style_1)
        text_2, style_2 = change_text_and_style(new_message_2, text_2, style_2)
        text_3, style_3 = change_text_and_style(new_message_3, text_3, style_3)
        text_4, style_4 = change_text_and_style(new_message_4, text_4, style_4)

        line_style_1 = 'line1_%d' % style_1
        line_style_2 = 'line2_%d' % style_2
        line_style_3 = 'line3_%d' % style_3
        line_style_4 = 'line4_%d' % style_4

        while True:
            counter_1 = print_line(text_1, lcd, line_style_1, counter_1, white)
            counter_2 = print_line(text_2, lcd, line_style_2, counter_2, white)
            counter_3 = print_line(text_3, lcd, line_style_3, counter_3, white)
            counter_4 = print_line(text_4, lcd, line_style_4, counter_4, white)

            if (q1.poll()) or (q2.poll()) or (q3.poll()) or (q4.poll()):
                break

            time.sleep(delay)


if __name__ == '__main__':
    pass
