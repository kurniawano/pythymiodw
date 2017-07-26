from pythymiodw import *
import time

class MyRobot(Thymio):
    def main_control(self):
	print self.get_prox_sensors_val()
	print self.get_temperature()
	print self.get_accelerometer()

m=MyRobot()
m.run()

