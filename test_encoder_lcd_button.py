# encoding:utf-8


from hardware.rotary import RotaryEncoder_proc
from hardware.rotary.RotaryEncoder_proc import REException
from hardware.lcd import LCD_proc
from multiprocessing import Queue


def stop_all(state):
    if (state['button_1'] == True) and (state['button_3'] == True):
        return True


def button(line, state, message, id):
    if message['button'] == 1:
        line.put({'text': 'button '+str(id)+' down', 'style': 'center'})
        state['button_'+str(id)] = True
    elif message['button'] == 0:
        line.put({'text': 'button '+str(id)+' up', 'style': 'center'})
        state['button_'+str(id)] = False
    else:
        raise REException('Unexpected button state.')

    return state


def main():
    line_1 = Queue()
    line_2 = Queue()
    line_3 = Queue()
    line_4 = Queue()
    encoders = Queue()

    line_1.put({'text':'', 'style':'center'})
    line_2.put({'text':'', 'style':'center'})
    line_3.put({'text':'', 'style':'center'})
    line_4.put({'text':'', 'style':'center'})

    print 'RE#1'
    pe1 = RotaryEncoder_proc.RE_runner(encoders, 1, 7, 9, 8)
    print 'RE#2'
    pe2 = RotaryEncoder_proc.RE_runner(encoders, 2, 0, 2, 3)
    print 'RE#3'
    pe3 = RotaryEncoder_proc.RE_runner(encoders, 3, 12, 13, 14)
    print 'LCD'
    plcd = LCD_proc.LCD_runner(line_1, line_2, line_3, line_4)

    sum_1 = sum_2 = sum_3 = 0
    state = {'button_1': False, 'button_2': False, 'button_3': False}

    while True:
        encoder_message = encoders.get(block=True)
        if encoder_message['name'] == 1:
            if 'rot' in encoder_message:
                sum_1 += encoder_message['rot']
                line_1.put({'text':sum_1, 'style':'center'})
            elif 'button' in encoder_message:
                state = button(line_1, state, encoder_message, 1)
            else:
                raise REException('Unexpected RE behavior.')
        elif encoder_message['name'] == 2:
            if 'rot' in encoder_message:
                sum_2 += encoder_message['rot']
                line_2.put({'text':sum_2, 'style':'center'})
            elif 'button' in encoder_message:
                state = button(line_2, state, encoder_message, 2)
            else:
                raise REException('Unexpected RE behavior.')
        elif encoder_message['name'] == 3:
            if 'rot' in encoder_message:
                sum_3 += encoder_message['rot']
                line_3.put({'text':sum_3, 'style':'center'})
            elif 'button' in encoder_message:
                state = button(line_3, state, encoder_message, 3)
            else:
                raise REException('Unexpected RE behavior.')
        else:
            raise REException('Unexpected encoder name.')

        if stop_all(state):
            break

    pe1.terminate()
    pe2.terminate()
    pe3.terminate()
    plcd.terminate()



if __name__ == '__main__':
    main()
