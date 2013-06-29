# encoding:utf-8


from hardware.rotary import RotaryEncoder_proc
from hardware.rotary.RotaryEncoder_proc import REException
from hardware.lcd import LCD_proc
from multiprocessing import Queue

import time

def on_startup():
    time.sleep(1)

    line_1 = Queue()
    line_2 = Queue()
    line_3 = Queue()
    line_4 = Queue()
    encoders = Queue()

    line_1.put({'text':'', 'style':'center'})
    line_2.put({'text':'3Radio', 'style':'center'})
    line_3.put({'text':'------', 'style':'center'})
    line_4.put({'text':'', 'style':'center'})

    pe1 = RotaryEncoder_proc.RE_runner(encoders, 1, 8, 9, 7)
    pe2 = RotaryEncoder_proc.RE_runner(encoders, 2, 0, 2, 3)
    pe3 = RotaryEncoder_proc.RE_runner(encoders, 3, 12, 13, 14)

    plcd = LCD_proc.LCD_runner(line_1, line_2, line_3, line_4)

    state = {'button_1': False,
             'button_2': False,
             'button_3': False,
             're_1': 0,
             're_2': 80,
             're_3': 0
    }
    
    lines = [line_1, line_2, line_3, line_4]
    encoders_proces = [pe1, pe2, pe3]
    
    main(state, encoders_proces, lines, encoders)


def terminate_all(lines, encoders_proces):
    lines[3].put({'stop': None})
    for ep in encoders_proces:
        ep.terminate()


def stop_all(state):
    if (state['button_1'] == True) and (state['button_3'] == True):
        return True


def on_button(state, message, id):
    if message['button'] == 1:
        state['button_'+str(id)] = True
    elif message['button'] == 0:
        state['button_'+str(id)] = False
    else:
        raise REException('Unexpected button state.')
    return state


def re_event(state, message):
    if 'rot' in message:
        state['re_' + str(message['name'])] += message['rot']
    elif 'button' in message:
        state = on_button(state, message, message['name'])
    else:
        raise REException('Unexpected Rotary Encoder message.')


def main(state, encoders_proces, lines, input):
    def line(id, text):
        lines[id-1].put({'text': str(text), 'style': 'center'})

    message = input.get(block=True)
    while True:
        if message['dev'] == 're':
            re_event(state, message)
        if stop_all(state):
            break
        
        message = input.get(block=True)

    terminate_all(lines, encoders_proces)


if __name__ == '__main__':
    on_startup()
