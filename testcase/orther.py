import sys

import uiautomator2 as u2
import time

from runlog.testLog import startLog

startLog()
def t1():
    print('123')
    print('被'+sys._getframe(1).f_code.co_name+'调用')

def t2():
    t1()
    print('456')

t2()