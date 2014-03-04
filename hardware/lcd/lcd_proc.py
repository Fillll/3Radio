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


def get_messages(pipes, counters):
    messages = [None, None, None, None]
    for each in range(4):
        while pipes[each].poll():
            message = Display()
            message.ParseFromString(pipes[each].recv())
            messages[each] = message
            counters[each] = 0
    return messages, counters


def change_text(messages, texts, styles):
    for each in range(4):
        if messages[each] is not None:
            texts[each] = messages[each].text
            styles[each] = messages[each].style
    return texts, styles


def print_line(text, lcd, line_style, counter, white):
    if len(text) <= lcd.LCD_WIDTH:
        to_print = text
    else:
        text = '%s%s%s' % (white, text, white)
        if counter == len(text) - lcd.LCD_WIDTH + 1:
            counter = 1
        to_print = text[counter:]
        counter += 1

    lcd.lcd_string(to_print, line_style)

    return counter

def print_lines(texts, styles, lcd, counters, white):
    for each in range(4):
        if len(texts[each]) <= lcd.LCD_WIDTH:
            to_print = texts[each]
        else:
            text = '%s%s%s' % (white, texts[each], white)
            if counters[each] == len(texts[each]) - lcd.LCD_WIDTH + 1:
                counters[each] = 1
            to_print = text[counters[each]:]
            counters[each] += 1
        getattr(lcd, 'line%d_%d' % (each + 1, styles[each]))(to_print)
    return counters


def LCD_worker(q1, q2, q3, q4, lcd, white=5, delay=0.5):
    """
    """
    in_pipes = [q1, q2, q3, q4]
    white = ' ' * white  # Whiting length
    counters = [0, 0, 0, 0]
    texts = ['1', '2', '3', '4']
    styles = [1, 1, 1, 1]

    while True:
        new_messages, counters = get_messages(in_pipes, counters)

        # if isinstance(new_message_4, dict):
        #     if 'stop' in new_message_4:
        #         break

        texts, styles = change_text(new_messages, texts, styles)

        while True:
            counters = print_lines(texts, styles, lcd, counters, white)

            if (q1.poll()) or (q2.poll()) or (q3.poll()) or (q4.poll()):
                break

            time.sleep(delay)


if __name__ == '__main__':
    pass
