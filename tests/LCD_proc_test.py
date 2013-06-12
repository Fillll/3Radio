# encoding: utf-8

from collections import deque
from multiprocessing import Process, Queue
from ..hardware.lcd import LCD_proc
import random
import time

if __name__ == '__main__':
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    q4 = Queue()

    q1.put('Hello world!!!')

    LCD_proc.LCD_runner(q1, q2, q3, q4)
    
    print 'TEST 1'
    q1.put('Hello world!')
    print 'TEST 2'

    for counter in range(4):
        time.sleep(4)
        i = random.randint(1,100)
        print str(i)
        q1.put(str(i))
        q2.put(str(i))
        q3.put(str(i))
        q4.put(str(i))

    time.sleep(2)
    q1.put('End...')
