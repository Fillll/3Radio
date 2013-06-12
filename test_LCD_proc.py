# encoding: utf-8

from multiprocessing import Queue
from hardware.lcd import LCD_proc
import random
import time


def test_LCD_proc():
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    q4 = Queue()

    q1.put({"text":'Hello world!!!','style':'center'})
    q2.put({"text":'line2', 'style':'center'})
    q3.put({"text":'line3 test', 'style':'center'})
    q4.put({"text":'last line test', 'style':'center'})

    LCD_proc.LCD_runner(q1, q2, q3, q4)
    
    print 'TEST 1'
    q1.put({"text":'Hi!','style':'center'})
    print 'TEST 2'

    for counter in range(4):
        time.sleep(4)
        i = random.randint(1,100)
        print str(i)
        q1.put({"text":str(i),'style':'center'})
        q2.put({"text":str(i),'style':'center'})
        q3.put({"text":str(i),'style':'center'})
        q4.put({"text":str(i),'style':'center'})

    time.sleep(2)
    q1.put('End...')


if __name__ == '__main__':
    test_LCD_proc()
