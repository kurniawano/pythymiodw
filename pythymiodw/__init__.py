import time
#from robots import GenericRobot
#from robots.decorators import action, lock
#from robots.resources import Resource
#from robots.signals import ActionCancelled

import dbus
import dbus.mainloop.glib
import gobject
import sys
from optparse import OptionParser

#time step, 0.1 second
dt = 100

class Thymio(object):
    def __init__(self):
        #super(Thymio,self).__init__()
	self.device="thymio-II"
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus=dbus.SessionBus()
        self.network=dbus.Interface(self.bus.get_object('ch.epfl.mobots.Aseba','/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
	print self.network.GetNodesList()
	self.prox_sensors_val=[0,0,0,0,0,0,0]
	self.accelerometer=[0,0,0]
	self.temperature=0.0
	self.loop=gobject.MainLoop()
	self.handle=gobject.timeout_add(dt, self.main_control)

    def run(self):
	self.loop.run()

    def main_control(self):
	pass

    def get_prox_sensors_handler(self, r):
	self.prox_sensors_val=r

    def get_acc_handler(self, r):
	self.accelerometer=r

    def get_temperature_handler(self, r):
	self.temperature=r

    def get_variables_error(self, e):
        print 'error:'
	print str(e)
	self.loop.quit()

    def get_prox_sensors_val(self):
	self.network.GetVariable(self.device,"prox.horizontal", reply_handler=self.get_prox_sensors_handler, error_handler=self.get_variables_error)
	return self.prox_sensors_val

    def wheels(self,l,r):
	self.network.SetVariable(self.device,"motor.left.target",[l])
	self.network.SetVariable(self.device,"motor.right.target",[r])

    def halt(self):
	self.network.SetVariable(self.device,"motor.left.target",[0])
	self.network.SetVariable(self.device,"motor.right.target",[0])
	
    def get_temperature(self):
	self.network.GetVariable(self.device,"temperature", reply_handler=self.get_temperature_handler, error_handler=self.get_variables_error)
	return self.temperature

    def get_accelerometer(self):
	self.network.GetVariable(self.device,"acc", reply_handler=self.get_acc_handler, error_handler=self.get_variables_error)
	return self.accelerometer
