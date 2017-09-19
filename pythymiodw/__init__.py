from __future__ import print_function
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
from io import ProxGround

#time step, 0.1 second
dt = 100

class Thymio(object):
    def __init__(self):
	self.open()
	self._prox_horizontal=[0,0,0,0,0,0,0]
	self._prox_ground_delta=[0,0]
	self._prox_ground_reflected=[0,0]
	self._prox_ground_ambiant=[0,0]
	self._accelerometer=[0,0,0]
	self._temperature=0.0
	self.off_leds()
	self.off_sounds()

    def run(self):
	try:
	    self._run()
	except:
	    self.quit()

    def _run(self):
	pass

    def init_read(self):
	self.thread=Thread(target=self.run)
	self.thread.start()

    def open(self):
	pass    

    def close(self):
	print('closing.')
	time.sleep(2)

    def main_loop(self):
	self.get_prox_horizontal()
	self.get_prox_ground()
	self.get_temperature()
	self.get_accelerometer()
	return True

    def leds_top(self,r=0,g=0,b=0):
	pass

    def leds_circle(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
	pass

    def leds_buttons(self,led0=0, led1=0, led2=0, led3=0):
	pass

    def leds_prox_h(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
	pass

    def leds_prox_v(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
	pass

    def leds_rc(self,led=0):
	pass

    def leds_bottom_left(self,r=0,g=0,b=0):
	pass

    def leds_bottom_right(self,r=0,g=0,b=0):
	pass

    def leds_temperature(self,r=0,b=0):
	pass

    def leds_sound(self,led=0):
	pass

    def sound_system(self,n=0):
	pass

    def sound_freq(self,hz=0, ds=0):
	pass

    def sound_play(self,n=0):
	pass

    def sound_replay(self,n=0):
	pass

    def dbus_reply(self):
	pass

    def dbus_error(self, e):
        print('error:')
	print(str(e))

    def prox_horizontal_handler(self, r):
	dist=[int(x) for x in r]
	self._prox_horizontal=dist

    def prox_ground_delta_handler(self, r):
	self._prox_ground_delta=r

    def prox_ground_reflected_handler(self, r):
	self._prox_ground_reflected=r

    def prox_ground_ambiant_handler(self, r):
	self._prox_ground_ambiant=r

    def acc_handler(self, r):
	self._accelerometer=r

    def temperature_handler(self, r):
	t=[int(x) for x in r]
	self._temperature=t[0]/10.0

    def get_variables_error(self, e):
        print('error:')
	print(str(e))

    def get_prox_horizontal(self):
	pass

    def get_prox_ground_delta(self):
	pass

    def get_prox_ground_reflected(self):
	pass

    def get_prox_ground_ambiant(self):
	pass

    def get_prox_ground(self):
	self.get_prox_ground_delta()
	self.get_prox_ground_reflected()
	self.get_prox_ground_ambiant()
	return ProxGround(delta=self._prox_ground_delta, reflected=self._prox_ground_reflected, ambiant=self._prox_ground_ambiant)

    def read_prox_horizontal(self):
	return self._prox_horizontal

    def read_prox_ground(self):
	return ProxGround(delta=self._prox_ground_delta, reflected=self._prox_ground_reflected, ambiant=self._prox_ground_ambiant)

    def read_temperature(self):
	return self._temperature

    def read_accelerometer(self):
	return self._accelerometer

    def wheels(self,l,r):
	self._wheels(l,r)

    def _wheels(self,l,r):
	pass

    def halt(self):
	self._halt()

    def _halt(self):
	pass
	
    def off_leds(self):
	self.leds_top()
	self.leds_circle()
	self.leds_buttons()
	self.leds_prox_h()
	self.leds_prox_v()
	self.leds_rc()
	self.leds_bottom_left()
	self.leds_bottom_right()
	self.leds_temperature()
	self.leds_sound()

    def off_sounds(self):
	self.sound_system(-1)
	self.sound_freq()
	self.sound_play(-1)
	self.sound_replay(-1)

    def quit(self):
	self.halt()
	self.off_leds()
	self.off_sounds()
	self.quit_loop()
	self.close()

    def quit_loop(self):
	pass

    def get_temperature(self):
	pass

    def get_accelerometer(self):
	pass

    prox_horizontal=property(read_prox_horizontal)
    prox_ground=property(read_prox_ground)
    temperature=property(read_temperature)
    accelerometer=property(read_accelerometer)

class ThymioReal(Thymio):
    def open(self):
	self.device="thymio-II"
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus=dbus.SessionBus()
        self.aseba_proc=subprocess.Popen(['asebamedulla "ser:name=Thymio-II"'], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)	
	time.sleep(2)
        self.network=dbus.Interface(self.bus.get_object('ch.epfl.mobots.Aseba','/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
	node=self.network.GetNodesList()
	progress=0
	print('connecting: {:d}. \r'.format(progress),end='')
	while node==[]:
            self.network=dbus.Interface(self.bus.get_object('ch.epfl.mobots.Aseba','/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
	    node=self.network.GetNodesList()
	    sys.stdout.write('connecting: %d. \r'% progress)
	    sys.stdout.flush()
	    progress+=1
	print()
	print('connected to {:s}.'.format(node))
	self.network.LoadScripts(os.path.dirname(os.path.realpath(__file__))+'/thymiohandlers.aesl')
	self.loop=gobject.MainLoop()
	self.handle=gobject.timeout_add(dt, self.main_loop)

    def close(self):
	Thymio.close(self)
	os.killpg(os.getpgid(self.aseba_proc.pid), signal.SIGTERM)

    def _run(self):
        self.loop.run()

    def get(self, node, var):
	dbus_array = self.network.GetVariable(node, var)
	size = len(dbus_array)
	if (size==1):
	    return int(dbus_array[0])
	else:
	    return [int(dbus_array[x]) for x in range(0,size)]

    def set(self, node, var, value):
	self.network.SetVariable(node,var,value)

    def send_event_name(self, event_name, event_args):
	self.network.SendEventName(event_name, event_args, reply_handler=self.dbus_reply, error_handler=self.dbus_error)

    def leds_top(self,r=0,g=0,b=0):
	self.send_event_name('SetLEDsTop', [r,g,b])

    def leds_circle(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
	self.send_event_name('SetLEDsCircle', [led0, led1, led2, led3, led4, led5, led6, led7])

    def leds_buttons(self,led0=0, led1=0, led2=0, led3=0):
	self.send_event_name('SetLEDsButtons', [led0, led1, led2, led3])

    def leds_prox_h(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
	self.send_event_name('SetLEDsProxH', [led0, led1, led2, led3, led4, led5, led6, led7])

    def leds_prox_v(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
	self.send_event_name('SetLEDsProxV', [led0, led1, led2, led3, led4, led5, led6, led7])

    def leds_rc(self,led=0):
	self.send_event_name('SetLEDsRC', [led])

    def leds_bottom_left(self,r=0,g=0,b=0):
	self.send_event_name('SetLEDsBottomLeft', [r,g,b])

    def leds_bottom_right(self,r=0,g=0,b=0):
	self.send_event_name('SetLEDsBottomRight', [r,g,b])

    def leds_temperature(self,r=0,b=0):
	self.send_event_name('SetLEDsTemperature', [r,b])

    def leds_sound(self,led=0):
	self.send_event_name('SetLEDsSound', [led])

    def sound_system(self,n=0):
	self.send_event_name('SetSoundSystem', [n])

    def sound_freq(self,hz=0, ds=0):
	self.send_event_name('SetSoundFreq', [hz,ds])

    def sound_play(self,n=0):
	self.send_event_name('SetSoundPlay', [n])

    def sound_replay(self,n=0):
	self.send_event_name('SetSoundReplay', [n])

    def dbus_reply(self):
	pass

    def dbus_error(self, e):
	Thymio.dbus_error(self,e)
	self.quit()


    def get_variables_error(self, e):
	Thymio.get_variables_error(self,e)
	self.quit()

    def get_prox_horizontal(self):
	self.network.GetVariable(self.device,"prox.horizontal", reply_handler=self.prox_horizontal_handler, error_handler=self.get_variables_error)
	return self._prox_horizontal

    def get_prox_ground_delta(self):
	self.network.GetVariable(self.device,"prox.ground.delta", reply_handler=self.prox_ground_delta_handler, error_handler=self.get_variables_error)
	return self._prox_ground_delta

    def get_prox_ground_reflected(self):
	self.network.GetVariable(self.device,"prox.ground.reflected", reply_handler=self.prox_ground_reflected_handler, error_handler=self.get_variables_error)
	return self._prox_ground_reflected

    def get_prox_ground_ambiant(self):
	self.network.GetVariable(self.device,"prox.ground.ambiant", reply_handler=self.prox_ground_ambiant_handler, error_handler=self.get_variables_error)
	return self._prox_ground_ambiant

    def get_temperature(self):
	self.network.GetVariable(self.device,"temperature", reply_handler=self.temperature_handler, error_handler=self.get_variables_error)
	return self._temperature

    def get_accelerometer(self):
	self.network.GetVariable(self.device,"acc", reply_handler=self.acc_handler, error_handler=self.get_variables_error)
	return self._accelerometer


    def _wheels(self,l,r):
	self.set(self.device, "motor.left.target",[l])
	self.set(self.device, "motor.right.target",[r])

    def _halt(self):
	self.set(self.device, "motor.left.target", [0])
	self.set(self.device, "motor.right.target", [0])

    def quit_loop(self):
	self.loop.quit()
