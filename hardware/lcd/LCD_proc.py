# encoding:utf-8

import LCD
import time
from multiprocessing import Process

# Whiting length
white = 5
white = ' '*white

#LCD


def LCD_runner(q1, q2, q3, q4):
    '''
    Run proces for all 4 lines
    '''
    my_lcd = LCD.LCD20x4(26, 24, 22, 18, 16, 12, 10)

    p = Process(target=LCD_line_runner, args=(q1, my_lcd, 'line1_center'))
    p.start()
    time.sleep(5)

    # p = Process(target=LCD_line_runner, args=(q2, my_lcd, 'line2_center'))
    # p.start()

    # p = Process(target=LCD_line_runner, args=(q3, my_lcd, 'line3_center'))
    # p.start()

    # p = Process(target=LCD_line_runner, args=(q4, my_lcd, 'line4_center'))
    # p.start()


def LCD_line_runner(queue, lcd, line=None):
    if line == None:
        raise Exception('No such line (LCD_line_runner).')

    while True:
        string = queue.get(block=True)
        if (len(string) < lcd.LCD_WIDTH):
            # lcd.lineN_center(string)
            getattr(lcd, line)(string)
        else:
            string = '%s%s%s' % (white, string, white)

            while True:
                for i in range(len(string)-lcd.LCD_WIDTH+1):
                    string_WIDTH = string[i:]
                    getattr(lcd, line)(string_WIDTH)
                    time.sleep(0.5)
                    if not len(queue) == 0:
                        break
                if not len(queue) == 0:
                    break


if __name__ == '__main__':
    pass
