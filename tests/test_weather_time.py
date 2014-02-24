# -*- coding: utf-8 -*-

from multiprocessing import Queue, reduction, Pipe, current_process
import pylibmc

from hardware.rotary import rotary_encoder_proc
from hardware.rotary.rotary_encoder_proc import REException
from hardware.lcd import lcd_proc


def stop_all(state):
    if (state[1] == True) and (state[3] == True):
        return True


def button(line, state, message, encoder_id):
    if message['button'] == 1:
        line.send({'text': 'button %d is down' % encoder_id, 'style': 'center'})
        state[encoder_id] = True
    elif message['button'] == 0:
        line.send({'text': 'button %d is up' % encoder_id, 'style': 'center'})
        state[encoder_id] = False
    else:
        raise REException('Unexpected button state.')

    return state


def main():
    recv_1, send_1 = Pipe(duplex=False)
    recv_2, send_2 = Pipe(duplex=False)
    recv_3, send_3 = Pipe(duplex=False)
    recv_4, send_4 = Pipe(duplex=False)
    lines = {1: send_1, 2: send_2, 3: send_3}
    encoders = Queue()

    lines[1].send({'text': '3Radio', 'style': 'center'})
    lines[2].send({'text': '------', 'style': 'center'})
    lines[3].send({'text': '', 'style': 'center'})
    send_4.send({'text': 'Loading...', 'style': 'center'})

    # print 'RE#1'
    pe1 = rotary_encoder_proc.RE_runner(encoders, 1, 8, 9, 7)
    # print 'RE#2'
    pe2 = rotary_encoder_proc.RE_runner(encoders, 2, 0, 2, 3)
    # print 'RE#3'
    pe3 = rotary_encoder_proc.RE_runner(encoders, 3, 12, 13, 14)
    # print 'LCD'
    plcd = lcd_proc.LCD_runner(recv_1, recv_2, recv_3, recv_4)

    mc = pylibmc.Client(['127.0.0.1'], binary=True,
                                 behaviors={'tcp_nodelay': True,
                                 'ketama': True})
    mc['city'] = 'Moscow,ru'
    mc['TNWU_authkey'] = current_process().authkey
    mc['TNWU_reduced_connection'] = reduction.reduce_connection(send_4)
    mc['TNWU_running'] = False
    mc['TNWU_last_temp'] = '-666.666'

    amount = {1: 0, 2: 0, 3: 0}
    state = {1: False, 2: False, 3: False}

    while True:
        encoder_message = encoders.get(block=True)
        encoder_id = encoder_message['name']

        if 'rot' in encoder_message:
            amount[encoder_id] += encoder_message['rot']
            lines[encoder_id].send({'text': amount[encoder_id], 'style': 'center'})
        elif 'button' in encoder_message:
            state = button(lines[encoder_id], state, encoder_message, encoder_id)

        if stop_all(state):
            break

    pe1.terminate()
    pe2.terminate()
    pe3.terminate()
    plcd.terminate()


if __name__ == '__main__':
    main()
