import sys
#sys.path.append('..')

from pythymiodw import *

m=ThymioSimPG()
m.wheels(300,300)
m.sleep(1)
m.wheels(-300,300)
m.sleep(1)
m.wheels(300,-300)
m.sleep(1)
m.quit()

