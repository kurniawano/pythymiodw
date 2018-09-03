from __future__ import print_function
import sys
import time
#sys.path.append('..')
from pythymiodw import ThymioSimPG

m = ThymioSimPG(scale=3)
print('color top 1')
m.leds_top(0,0,32)
m.sleep(2)
print('color top 2')
m.leds_top(32,0,0)
m.sleep(2)

print('switch off.')
m.quit()

