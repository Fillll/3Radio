# encoding:utf-8

import LCD
import time
from multiprocessing import Process


def LCD_runner(q1, q2, q3, q4):
    '''
    Run proces for all 4 lines
    '''
    my_lcd = LCD.LCD20x4(26, 24, 22, 18, 16, 12, 10)

    p = Process(target=LCD_worker, args=(q1, q2, q3, q4, my_lcd))
    p.start()


def get_text_from(q, counter):
    if q.empty():
        return None, counter

    message = None
    while q.empty == False:
        print 'take one!'
        message = q.get()

    if message == None:
        message = {'text':'XM...', 'style':'center'}
    return message, 0


def change_text_and_style(message, text, style):
    if message is None:
        return text, style
    if style in ['center', 'time_temp']:
        return message['text'], message['style']


def print_line(text, lcd, line_style, counter):
    if len(text) < lcd.LCD_WIDTH:
        to_print = text
    else:
        if counter == len(text)-lcd.LCD_WIDTH+1:
            counter = 1
        to_print = text[counter:]
        counter += 1

    getattr(lcd, line_style)(to_print)

    return counter


def LCD_worker(q1, q2, q3, q4, lcd, white=5):
    """
    """

    # Whiting length
    white = ' '*white

    counter_1 = counter_2 = counter_3 = counter_4 = 0

    text_1 = text_2 = text_3 = text_4 = '0'

    style_1 = style_2 = style_3 = style_4 = 'center'

    while True:
        new_message_1, counter_1 = get_text_from(q1, counter_1)
        new_message_2, counter_2 = get_text_from(q2, counter_2)
        new_message_3, counter_3 = get_text_from(q3, counter_3)
        new_message_4, counter_4 = get_text_from(q4, counter_4)

        text_1, style_1 = change_text_and_style(new_message_1, text_1, style_1)
        text_2, style_2 = change_text_and_style(new_message_2, text_2, style_2)
        text_3, style_3 = change_text_and_style(new_message_3, text_3, style_3)
        text_4, style_4 = change_text_and_style(new_message_4, text_4, style_4)

        line_style_1 = 'line1_%s' % style_1
        line_style_2 = 'line2_%s' % style_2
        line_style_3 = 'line3_%s' % style_3
        line_style_4 = 'line4_%s' % style_4

        counter_1 = print_line(text_1, lcd, line_style_1, counter_1)
        counter_2 = print_line(text_2, lcd, line_style_2, counter_2)
        counter_3 = print_line(text_3, lcd, line_style_3, counter_3)
        counter_4 = print_line(text_4, lcd, line_style_4, counter_4)


# def LCD_line_runner(queue, lcd, line=None):
#     if line == None:
#         raise Exception('No such line (LCD_line_runner).')

#     while True:
#         string = queue.get(block=True)
#         if (len(string) < lcd.LCD_WIDTH):
#             # lcd.lineN_center(string)
#             getattr(lcd, line)(string)
#         else:
#             string = '%s%s%s' % (white, string, white)

#             while True:
#                 for i in range(len(string)-lcd.LCD_WIDTH+1):
#                     string_WIDTH = string[i:]
#                     getattr(lcd, line)(string_WIDTH)
#                     time.sleep(0.5)
#                     if not len(queue) == 0:
#                         break
#                 if not len(queue) == 0:
#                     break


if __name__ == '__main__':
    pass
