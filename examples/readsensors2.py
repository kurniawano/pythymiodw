from pythymiodw import *
import time


m=Thymio()
while(1):
    print m.get_temperature()
    time.sleep(1)
    print m.get_prox_sensors_val()
    time.sleep(1)


