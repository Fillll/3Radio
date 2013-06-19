# encoding:utf-8


from hardware.rotary import RotaryEncoder_proc
from hardware.rotary.RotaryEncoder_proc import REException
from multiprocessing import Queue


def main():
    q = Queue()

    RotaryEncoder_proc.RE_runner(q, 1, 7, 9, 8)

    while True:
        result = q.get(block=True)
        if 'rot' in result:
            print '%s: %s' % (str(result['name']), str(result['rot']))
        elif 'button' in result:
            print '%s: %s' % (str(result['name']), str(result['button']))
        else:
            raise REException('Unexpected message.')


if __name__ == '__main__':
    main()
