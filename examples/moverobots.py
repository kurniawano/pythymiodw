import sys
#sys.path.append('..')

from pythymiodw import *
import time


m=Thymio()
m.init_read()
m.wheels(300,300)
time.sleep(1)
m.wheels(-300,300)
time.sleep(1)
m.wheels(300,-300)
time.sleep(1)
m.quit()

