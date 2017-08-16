import sys
import time
#sys.path.append('..')
from pythymiodw import ThymioReal

m=ThymioReal()
m.init_read()
for i in range(4):
    m.wheels(100,100)
    time.sleep(2)
    m.wheels(0,0)
    time.sleep(1)

m.quit()
