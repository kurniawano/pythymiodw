import sys
#sys.path.append('..')

from pythymiodw import Thymio
import time


m=Thymio()
m.init_read()
print m.prox_sensors_val
print m.temperature
print m.accelerometer
time.sleep(1)
print m.prox_sensors_val
print m.temperature
print m.accelerometer
m.quit()
