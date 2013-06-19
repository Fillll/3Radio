# encoding:utf-8


from hardware.rotary.RotaryEncoder import RotaryEncoder_proc, REException
from hardware.lcd import LCD_proc
from multiprocessing import Queue


def main():
    line_1 = Queue()
    line_2 = Queue()
    line_3 = Queue()
    line_4 = Queue()
    encoders = Queue()

    line_1.put('text':'', 'style':'center')
    line_2.put('text':'', 'style':'center')
    line_3.put('text':'', 'style':'center')
    line_4.put('text':'', 'style':'center')

    RotaryEncoder_proc.RE_runner(encoders, 1, 7, 9, 8)
    # RotaryEncoder_proc.RE_runner(encoders, 2, x, y, z)
    # RotaryEncoder_proc.RE_runner(encoders, 3, z, y, z)

    LCD_proc.LCD_runner(line_1, line_2, line_3, line_4)

    sum_1 = sum_2 = sum_3 = 0

    while True:
        encoder_message = encoders.get(block=True)
        if encoder_message['name'] == 1:
            sum_1 += encoder_message['rot']
            line_1.put({'text':sum_1, 'style':'center'})
        elif encoder_message['name'] == 2:
            sum_2 += encoder_message['rot']
            line_2.put({'text':sum_2, 'style':'center'})
        elif encoder_message['name'] == 3:
            sum_3 += encoder_message['rot']
            line_3.put({'text':sum_3, 'style':'center'})
        else:
            raise REException('Unexpected encoder name.')


if __name__ == '__main__':
    main()