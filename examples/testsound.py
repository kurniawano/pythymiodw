from __future__ import print_function
import sys

#sys.path.append('..')
from pythymiodw import ThymioReal

m=ThymioReal()
m.init_read()
print('sound.system(7)')
m.sound_system(7)
m.sleep(2)
m.sound_system(-1)
m.sleep(2)
print('sound.freq(440,2)')
m.sound_freq(440,2)
m.sleep(2)
m.sound_freq()
m.sleep(2)
m.quit()
