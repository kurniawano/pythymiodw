from __future__ import print_function
import sys
import time
#sys.path.append('..')
from pythymiodw import ThymioReal

m = ThymioReal()
while True:
    print('color top 1')
    m.leds_top(0,0,32)
    m.sleep(0.5)
    f=m.button_forward
    b=m.button_backward
    if b:
        break
    if f:
        print('forward')
m.quit()

