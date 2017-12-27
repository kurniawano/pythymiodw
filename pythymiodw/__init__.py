from __future__ import print_function
from __future__ import absolute_import
import time
import subprocess
import os
import sys
import signal
import turtle

import dbus
import dbus.mainloop.glib
#import gobject
from gi.repository import GObject as gobject
from optparse import OptionParser
from threading import Thread
from . import io 
from .world import Point
#import queue
import math

#time step, 0.1 second
dt = 200

class Thymio:
    """ This is the base class for Thymio.

    You never need to instantiate this class directly. Use ThymioReal or ThymioSim instead.
    """
    def __init__(self):
    """Constructor need not any argument.
    """
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
    """A method to start the robot. You need not call this directly. It is called by init_read() method.

    This method calls _run() which is implemented in ThymioReal and ThymioSim.
    """
        try:
            self._run()
        except Exception as inst:
            print('Fail running thread.')
            print(type(inst))
            print(inst.args)
            print(inst)
            self.quit()

    def _run(self):
    """Internal method to run the robot. This is called by run() and implemented by ThymioReal and ThymioSim.
    """
        pass

    def init_read(self):
    """Method to start running the robot in a thread. It calls run().
    """
        self.thread=Thread(target=self.run)
        self.thread.start()

    def open(self):
    """Method to open the connection. Implemented in the subclass.
    """
        pass    

    def close(self):
    """Method to be called when closing. You need not call this directly. ThymioReal and ThymioSim implements this.
    """
        print('closing.')
        time.sleep(2)

    def main_loop(self):
    """Main loop to be called every time stelp.

    The main loop simply reads the various sensors and returns True.
    """
        self.get_prox_horizontal()
        self.get_prox_ground()
        self.get_temperature()
        self.get_accelerometer()
        return True

    def leds_top(self,r=0,g=0,b=0):
    """Turn on top LEDs. Implemented in sub class.
    """
        pass

    def leds_circle(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
    """Turn on circle LEDs. Implemented in sub class.
    """
        pass

    def leds_buttons(self,led0=0, led1=0, led2=0, led3=0):
    """Turn on LEDs on buttons. Implemented in sub class.
    """
        pass

    def leds_prox_h(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
    """Turn on horizontal proximity sensors' LEDs. Implemented in sub class.
    """
        pass

    def leds_prox_v(self,led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0):
    """Turn on vertical proximity sensors' LEDs. Implemented in sub class.
    """
        pass

    def leds_rc(self,led=0):
    """Turn on RC LED. Implemented in sub class.
    """
        pass

    def leds_bottom_left(self,r=0,g=0,b=0):
    """Turn on LED on bottom left of robot. Implemented in sub class.
    """
        pass

    def leds_bottom_right(self,r=0,g=0,b=0):
    """Turn on LED on bottom right of robot. Implemented in sub class.
    """
        pass

    def leds_temperature(self,r=0,b=0):
    """Turn on temperature sensor's LED of robot. Implemented in sub class.
    """
        pass

    def leds_sound(self,led=0):
    """Turn on speaker's LED of robot. Implemented in sub class.
    """
        pass

    def sound_system(self,n=0):
    """Turn on the sound for system. Implemented in sub class.
    """
        pass

    def sound_freq(self,hz=0, ds=0):
    """Turn on sound using specific frequency. Implemented in sub class.
    """
        pass

    def sound_play(self,n=0):
    """Play recorded sound. Implemented in sub class.
    """
        pass

    def sound_replay(self,n=0):
        pass

    def dbus_error(self, e):
        print('error:')
        print(str(e))

    def prox_horizontal_handler(self, r):
        dist=[int(x) for x in r]
        self._prox_horizontal=dist

    def prox_ground_delta_handler(self, r):
        t=[int(x) for x in r]
        self._prox_ground_delta=t

    def prox_ground_reflected_handler(self, r):
        t=[int(x) for x in r]
        self._prox_ground_reflected=t

    def prox_ground_ambiant_handler(self, r):
        t=[int(x) for x in r]
        self._prox_ground_ambiant=t

    def acc_handler(self, r):
        t=[int(x) for x in r]
        self._accelerometer=t

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
        return io.ProxGround(delta=self._prox_ground_delta, reflected=self._prox_ground_reflected, ambiant=self._prox_ground_ambiant)

    def read_prox_horizontal(self):
        return self._prox_horizontal

    def read_prox_ground(self):
        return io.ProxGround(delta=self._prox_ground_delta, reflected=self._prox_ground_reflected, ambiant=self._prox_ground_ambiant)

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
        print('connected to {!s:s}.'.format(node))
        self.network.LoadScripts(os.path.dirname(os.path.realpath(__file__))+'/thymiohandlers.aesl')
        self.loop=gobject.MainLoop()
        self.handle=gobject.timeout_add(dt, self.main_loop)

    def close(self):
        Thymio.close(self)
        os.killpg(os.getpgid(self.aseba_proc.pid), signal.SIGTERM)

    def _run(self):
        try:
            self.loop.run()
        except:
            self.quit()

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

    def sleep(self,n):
        time.sleep(n)

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

class ThymioSim(Thymio):
    def __init__(self,world=None):
        super().__init__()
        self.forward_velocity=0.0
        self.rotational_velocity=0.0
        self.leftv=0
        self.rightv=0
        self.heading=0.0
        self.world=world
        if self.world!=None:
            ll,ur=self.world.get_world_boundaries()
            self.window.setworldcoordinates(ll.x,ll.y,ur.x,ur.y)
            self.world.draw_world(self.robot)
            self.init_pos=self.world.get_init_pos()
            self.heading=self.world.get_init_heading()
        else:
            self.init_pos=Point(0,0)
            self.heading=0
        self.robot.setposition(self.init_pos.x,self.init_pos.y)
        self.robot.setheading(self.heading)
        #self.run()

    def open(self):
        self.window=turtle.Screen()
        self.robot=turtle.Turtle()
        #self.robot.penup()
        
        
    def run(self):
        #output=io.Action(fv=self.forward_velocity,rv=self.rotational_velocity)
        self.get_prox_horizontal()
        self._wheels(self.leftv,self.rightv)
        #turtle.ontimer(self.run,100)
        
    def wheels(self, l, r):
        self.leftv=l
        self.rightv=r
        
    def speed_to_pixel(self, l,r):
        vl=20/500.0*l*dt/1000 #20cm/s divided by max speed wheels 500
        vr=20/500.0*r*dt/1000
        return vl, vr

    def sleep(self,n):
        t=0
        while t<n:
            self.run()
            t+=0.1
            time.sleep(0.1)
    def rad_to_deg(self,omega):
        return omega/math.pi*180
    
    def _wheels(self,l,r):
        W=0.095*100
        vl,vr=self.speed_to_pixel(l,r)
        omega=1/W*(vr-vl)
        omegadeg=self.rad_to_deg(omega)
        fv=0.5*(vr+vl)
        self.heading+=omegadeg
        can_move=self.check_world(fv)
        if can_move:
            self.robot.forward(fv)
        self.robot.setheading(self.heading)
      
    def check_world(self, fv):
        if self.world==None:
            return True
        rad=fv*dt/1000.0
        new_x, new_y = self.get_new_point(rad)
        if self.world.is_overlap(Point(new_x,new_y)):
            return False
        ll,ur=self.world.get_world_boundaries()
        if new_x<ll.x or new_x > ur.x or new_y<ll.y or new_y>ur.y:
            return False
        return True
        
    def get_new_point(self,rad):
        angle=self.robot.heading()
        angle_rad=angle/180.0*math.pi  
        x,y=self.robot.position()
        dx=rad*math.cos(angle_rad)
        dy=rad*math.sin(angle_rad)
        new_x,new_y=x+dx,y+dy
        return new_x, new_y
      

    def get_prox_horizontal(self):
        rad=10 # when it is 10cm
        new_x, new_y=self.get_new_point(rad)
        self._prox_horizontal=[0 for i in range(7)]
        if self.world!=None:
            if self.world.is_overlap(Point(new_x,new_y)):
                self._prox_horizontal[2]=1000 
        return self._prox_horizontal
