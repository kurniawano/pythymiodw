from __future__ import print_function
import sys
#sys.path.append('..')

from pythymiodw import ThymioReal
import time


m=ThymioReal()
m.init_read()
print(m.prox_horizontal)
print(m.prox_ground)
print(m.temperature)
print(m.accelerometer)
time.sleep(1)
print(m.prox_horizontal)
print(m.prox_ground)
print(m.temperature)
print(m.accelerometer)
m.quit()
