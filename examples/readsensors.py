import sys
#sys.path.append('..')

from pythymiodw import *
import time

class MyRobot(ThymioReal):
    def main_loop(self):
	print m.get_temperature()
	time.sleep(1)
	print m.get_prox_horizontal_val()
	time.sleep(1)
	return True

try:
    m=MyRobot()
    m.run()
except:
    m.quit()


