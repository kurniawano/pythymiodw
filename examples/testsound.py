import sys
import time
#sys.path.append('..')
from pythymiodw import ThymioReal

m=ThymioReal()
m.init_read()
print 'sound.system(7)'
m.sound_system(7)
time.sleep(2)
m.sound_system(-1)
time.sleep(2)
print 'sound.freq(440,2)'
m.sound_freq(440,2)
time.sleep(2)
m.sound_freq()
time.sleep(2)
m.quit()
