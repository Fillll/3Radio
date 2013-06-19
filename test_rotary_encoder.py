# encoding:utf-8


from hardware.rotary.RotaryEncoder import RotaryEncoder_proc, REException
from multiprocessing import Queue


def main():
    q = Queue()

    RotaryEncoder_proc.RE_runner(q, 7, 9, 8, 1)

    while True:
        result = q.get(block=True)
        if 'rot' in result:
            print '%s: %s' % (str(result['name']), str(result['rot']))
        elif 'button' in result:
            pass
        else:
            raise REException('Unexpected message.')


if __name__ == '__main__':
    main()
