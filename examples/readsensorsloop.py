from __future__ import print_function
import sys
#sys.path.append('..')

from pythymiodw import ThymioReal
import time


m=ThymioReal()
try:
    while True:
        print(m.prox_horizontal)
        print(m.prox_ground)
        print(m.temperature)
        print(m.accelerometer)
        m.sleep(0.5)
except KeyboardInterrupt:
    m.quit()
