from __future__ import print_function
import sys
#sys.path.append('..')

from pythymiodw import ThymioReal
import time


m=ThymioReal()
print(m.prox_horizontal)
print(m.prox_ground.delta)
print(m.prox_ground.reflected)
print(m.prox_ground.ambiant)
print(m.temperature)
print(m.accelerometer)
m.sleep(3)
print(m.prox_horizontal)
print(m.prox_ground.delta)
print(m.prox_ground.reflected)
print(m.prox_ground.ambiant)
print(m.temperature)
print(m.accelerometer)
m.quit()
