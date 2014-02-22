# -*- coding: utf-8 -*-

from multiprocessing import Queue

from hardware.rotary import rotary_encoder_proc
from hardware.rotary.rotary_encoder_proc import REException
from hardware.lcd import lcd_proc
from software.weather_time import weather_time_runner


def stop_all(state):
    if (state[1] == True) and (state[3] == True):
        return True


def button(line, state, message, encoder_id):
    if message['button'] == 1:
        line.put({'text': 'button %d is down' % encoder_id, 'style': 'center'})
        state[encoder_id] = True
    elif message['button'] == 0:
        line.put({'text': 'button %d is up' % encoder_id, 'style': 'center'})
        state[encoder_id] = False
    else:
        raise REException('Unexpected button state.')

    return state


def main():
    line_1 = Queue()
    line_2 = Queue()
    line_3 = Queue()
    line_4 = Queue()
    lines = {1: line_1, 2: line_2, 3: line_3, 4: line_4}
    encoders = Queue()

    line_1.put({'text': '3Radio', 'style': 'center'})
    line_2.put({'text': '------', 'style': 'center'})
    line_3.put({'text': '', 'style': 'center'})
    line_4.put({'text': 'Loading...', 'style': 'center'})

    # print 'RE#1'
    pe1 = rotary_encoder_proc.RE_runner(encoders, 1, 8, 9, 7)
    # print 'RE#2'
    pe2 = rotary_encoder_proc.RE_runner(encoders, 2, 0, 2, 3)
    # print 'RE#3'
    pe3 = rotary_encoder_proc.RE_runner(encoders, 3, 12, 13, 14)
    # print 'LCD'
    plcd = lcd_proc.LCD_runner(line_1, line_2, line_3, line_4)

    p_wt = weather_time_runner(line_4, 'Moscow,ru')

    amount = {1: 0, 2: 0, 3: 0}
    state = {1: False, 2: False, 3: False}

    while True:
        encoder_message = encoders.get(block=True)
        encoder_id = encoder_message['name']

        if 'rot' in encoder_message:
            amount[encoder_id] += encoder_message['rot']
            lines[encoder_id].put({'text': amount[encoder_id], 'style': 'center'})
        elif 'button' in encoder_message:
            state = button(lines[encoder_id], state, encoder_message, encoder_id)

        if stop_all(state):
            break

    p_wt.terminate()
    pe1.terminate()
    pe2.terminate()
    pe3.terminate()
    plcd.terminate()


if __name__ == '__main__':
    main()
