from __future__ import print_function
import sys
#sys.path.append('..')

from pythymiodw import ThymioReal
import time


m=ThymioReal()
m.init_read()
while True:
    print(m.prox_horizontal)
    m.sleep(0.1)
m.quit()
