import sys
import time
#sys.path.append('..')
from pythymiodw import Thymio

m = Thymio()
m.init_read()
print 'color top 1'
m.leds_top(0,0,32)
time.sleep(2)
print 'color top 2'
m.leds_top(32,0,0)
time.sleep(2)
print 'circle led 0'
m.leds_circle(led0=32)
time.sleep(2)
print 'circle led 3'
m.leds_circle(led3=32)
time.sleep(2)
print 'button led 0'
m.leds_buttons(led0=32)
time.sleep(2)
print 'button led 2'
m.leds_buttons(led2=32)
time.sleep(2)
print 'prox h led 2'
m.leds_prox_h(led2=32)
time.sleep(2)
print 'prox v led 2'
m.leds_prox_v(led2=32)
time.sleep(2)
print 'led rc'
m.leds_rc(32)
time.sleep(2)
print 'led bottom left'
m.leds_bottom_left(0,32,0)
time.sleep(2)
print 'led bottom right'
m.leds_bottom_right(0,32,0)
time.sleep(2)
print 'led sound'
m.leds_sound(32)
time.sleep(2)
print 'led temperature'
m.leds_temperature(32,0)
time.sleep(2)
m.leds_prox_h(led2=32)
print 'switch off.'
m.quit()

