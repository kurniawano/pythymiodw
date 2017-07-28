import time
import subprocess
import os
import sys
import signal

import dbus
import dbus.mainloop.glib
import gobject
from optparse import OptionParser
from threading import Thread

#time step, 0.1 second
dt = 100

class Thymio(object):
    def __init__(self):
	self.open()
	self._prox_sensors_val=[0,0,0,0,0,0,0]
	self._accelerometer=[0,0,0]
	self._temperature=0.0
	self.loop=gobject.MainLoop()
	self.handle=gobject.timeout_add(dt, self.main_loop)

    def run(self):
	try:
	    self.loop.run()
	except:
	    self.quit()

    def init_read(self):
	self.thread=Thread(target=self.run)
	self.thread.start()

    def open(self):
	self.device="thymio-II"
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus=dbus.SessionBus()
        self.aseba_proc=subprocess.Popen(['asebamedulla "ser:name=Thymio-II"'], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)	
	time.sleep(2)
        self.network=dbus.Interface(self.bus.get_object('ch.epfl.mobots.Aseba','/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
	node=self.network.GetNodesList()
	progress=0
	print 'connecting: %d. \r'%progress,
	while node==[]:
            self.network=dbus.Interface(self.bus.get_object('ch.epfl.mobots.Aseba','/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
	    node=self.network.GetNodesList()
	    sys.stdout.write('connecting: %d. \r'% progress)
	    sys.stdout.flush()
	    progress+=1
	print
	print 'connected to %s.'%node
	    

    def close(self):
	print 'closing.'
	time.sleep(2)
	os.killpg(os.getpgid(self.aseba_proc.pid), signal.SIGTERM)

    def main_loop(self):
	self.get_prox_sensors_val()
	self.get_temperature()
	self.get_accelerometer()
	return True

    def get(self, node, var):
	dbus_array = self.network.GetVariable(node, var)
	size = len(dbus_array)
	if (size==1):
	    return int(dbus_array[0])
	else:
	    return [int(dbus_array[x]) for x in range(0,size)]

    def set(self, node, var, value):
	self.network.SetVariable(node,var,value)

    def prox_sensors_handler(self, r):
	self._prox_sensors_val=r

    def acc_handler(self, r):
	self._accelerometer=r

    def temperature_handler(self, r):
	self._temperature=r

    def get_variables_error(self, e):
        print 'error:'
	print str(e)
	self.loop.quit()

    def get_prox_sensors_val(self):
	self.network.GetVariable(self.device,"prox.horizontal", reply_handler=self.prox_sensors_handler, error_handler=self.get_variables_error)
	return self._prox_sensors_val

    def read_prox_sensors_val(self):
	return self._prox_sensors_val

    def read_temperature(self):
	return self._temperature

    def read_accelerometer(self):
	return self._accelerometer

    def wheels(self,l,r):
	self.set(self.device, "motor.left.target",[l])
	self.set(self.device, "motor.right.target",[r])

    def halt(self):
	self.set(self.device, "motor.left.target", [0])
	self.set(self.device, "motor.right.target", [0])
	
    def quit(self):
	self.halt()
	self.loop.quit()
	self.close()

    def get_temperature(self):
	self.network.GetVariable(self.device,"temperature", reply_handler=self.temperature_handler, error_handler=self.get_variables_error)
	return self._temperature

    def get_accelerometer(self):
	self.network.GetVariable(self.device,"acc", reply_handler=self.acc_handler, error_handler=self.get_variables_error)
	return self._accelerometer

    prox_sensors_val=property(read_prox_sensors_val)
    temperature=property(read_temperature)
    accelerometer=property(read_accelerometer)
