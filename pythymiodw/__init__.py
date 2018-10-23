from __future__ import print_function
from __future__ import absolute_import
import time
import subprocess
import os
import sys
import signal
import turtle
import pygame
import queue
import Pyro4
from threading import Thread
from . import io
from .world import Point, Line, Floor
from .pg import PGWindow, PGRobot
import math
import tkinter as tk
from PIL import ImageTk
if sys.platform == 'linux' or sys.platform == 'linux2':
    import dbus
    import dbus.mainloop.glib
    from gi.repository import GObject as gobject
else:
    import requests
    import json


# time step, 0.2 second
dt = 200


class Thymio:

    """ This is the base class for Thymio.

    You never need to instantiate this class directly.
    Use ThymioReal or ThymioSim instead.
    """

    def __init__(self):
        """Constructor need not any argument.
        """
        self.open()
        self._prox_horizontal = [0, 0, 0, 0, 0, 0, 0]
        self._prox_ground_delta = [0, 0]
        self._prox_ground_reflected = [0, 0]
        self._prox_ground_ambiant = [0, 0]
        self._accelerometer = [0, 0, 0]
        self._temperature = 0.0
        self._button_center = 0
        self._button_left = 0
        self._button_right = 0
        self._button_forward = 0
        self._button_backward = 0
        self.off_leds()
        self.off_sounds()

    def open(self):
        """Method to open the connection. Implemented in the subclass.
        """
        pass

    def close(self):
        """Method to be called when closing.
        You need not call this directly.
        ThymioReal and ThymioSim implements this.
        """
        print('closing.')
        time.sleep(2)

    def main_loop(self):
        """Main loop to be called every time step.

        The main loop simply reads the various sensors and returns True.
        """
        self.get_prox_horizontal()
        self.get_prox_ground()
        self.get_temperature()
        self.get_accelerometer()
        self.get_button_center()
        self.get_button_left()
        self.get_button_right()
        self.get_button_forward()
        self.get_button_backward()
        return True

    def leds_top(self, r=0, g=0, b=0):
        """Turn on top LEDs. Implemented in sub class.
        """
        pass

    def leds_circle(self, led0=0, led1=0, led2=0, led3=0,
                    led4=0, led5=0, led6=0, led7=0):
        """Turn on circle LEDs. Implemented in sub class.
        """
        pass

    def leds_buttons(self, led0=0, led1=0, led2=0, led3=0):
        """Turn on LEDs on buttons. Implemented in sub class.
        """
        pass

    def leds_prox_h(self, led0=0, led1=0, led2=0, led3=0,
                    led4=0, led5=0, led6=0, led7=0):
        """Turn on horizontal proximity sensors' LEDs.
        Implemented in sub class.
        """
        pass

    def leds_prox_v(self, led0=0, led1=0, led2=0, led3=0,
                    led4=0, led5=0, led6=0, led7=0):
        """Turn on vertical proximity sensors' LEDs.
        Implemented in sub class.
        """
        pass

    def leds_rc(self, led=0):
        """Turn on RC LED. Implemented in sub class.
        """
        pass

    def leds_bottom_left(self, r=0, g=0, b=0):
        """Turn on LED on bottom left of robot. Implemented in sub class.
        """
        pass

    def leds_bottom_right(self, r=0, g=0, b=0):
        """Turn on LED on bottom right of robot. Implemented in sub class.
        """
        pass

    def leds_temperature(self, r=0, b=0):
        """Turn on temperature sensor's LED of robot. Implemented in sub class.
        """
        pass

    def leds_sound(self, led=0):
        """Turn on speaker's LED of robot. Implemented in sub class.
        """
        pass

    def sound_system(self, n=0):
        """Turn on the sound for system. Implemented in sub class.
        """
        pass

    def sound_freq(self, hz=0, ds=0):
        """Turn on sound using specific frequency. Implemented in sub class.
        """
        pass

    def sound_play(self, n=0):
        """Play recorded sound. Implemented in sub class.
        """
        pass

    def sound_replay(self, n=0):
        pass

    def dbus_error(self, e):
        print('error:')
        print(str(e))

    def get_variables_error(self, e):
        print('error:')
        print(str(e))

    def get_prox_horizontal(self):
        """Method to get horizontal proxmity sensors. Implemented by sub class.
        """
        pass

    def get_prox_ground_delta(self):
        """Method to get delta ground proximity sensor. Implemented by sub class.
        """
        pass

    def get_prox_ground_reflected(self):
        """Method to get reflected ground proximity sensor. Implemented by sub class.
        """
        pass

    def get_prox_ground_ambiant(self):
        """Method to get ambient ground proximity sensor. Implemented by sub class.
        """
        pass

    def get_prox_ground(self):
        """Method to get all the three ground proximity sensor:
        delta, reflected, and ambiant.

        Returns: io.ProxGround object.
        """
        self.get_prox_ground_delta()
        self.get_prox_ground_reflected()
        self.get_prox_ground_ambiant()
        return io.ProxGround(delta=self._prox_ground_delta,
                             reflected=self._prox_ground_reflected,
                             ambiant=self._prox_ground_ambiant)

    def get_temperature(self):
        """Method to get temperature sensor data. Implemented by sub class.
        """
        pass

    def get_accelerometer(self):
        """Method to get accelerometer data. Implemented by sub class.
        """
        pass

    def get_button_center(self):
        """Method to get center button. Implemented by sub class.
        """
        pass

    def get_button_left(self):
        """Method to get left button. Implemented by sub class.
        """
        pass

    def get_button_right(self):
        """Method to get right button. Implemented by sub class.
        """
        pass

    def get_button_forward(self):
        """Method to get forward button. Implemented by sub class.
        """
        pass

    def get_button_backward(self):
        """Method to get backward button. Implemented by sub class.
        """
        pass

    def read_prox_horizontal(self):
        """Method to read horizontal proximity sensor. Used by property.
        """
        return self._prox_horizontal

    def read_prox_ground(self):
        """Method to read ground proximity sensor. Used by property.
        """
        return io.ProxGround(delta=self._prox_ground_delta,
                             reflected=self._prox_ground_reflected,
                             ambiant=self._prox_ground_ambiant)

    def read_temperature(self):
        """Method to read temperature sensor. Used by property.
        """
        return self._temperature

    def read_accelerometer(self):
        """Method to read accelerometer. Used by property.
        """
        return self._accelerometer

    def read_button_center(self):
        """Method to read center button. Used by property.
        """
        return self._button_center

    def read_button_left(self):
        """Method to read left button. Used by property.
        """
        return self._button_left

    def read_button_right(self):
        """Method to read right button. Used by property.
        """
        return self._button_right

    def read_button_forward(self):
        """Method to read forward button. Used by property.
        """
        return self._button_forward

    def read_button_backward(self):
        """Method to read backward button. Used by property.
        """
        return self._button_backward

    def wheels(self, l, r):
        """Method to set the left and right speed of robot's wheels.
        """
        self._wheels(l, r)

    def _wheels(self, l, r):
        """Internal method called by wheels(). Implemented by sub class.
        """
        pass

    def halt(self):
        """Method to stop the robot.
        """
        self._halt()

    def _halt(self):
        """Internal method to stop the robot. Implemented by sub class.
        """
        pass

    def off_leds(self):
        """Method to turn off all LEDs.
        """
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
        """Method to switch off the sounds.
        """
        self.sound_system(-1)
        self.sound_freq()
        self.sound_play(-1)
        self.sound_replay(-1)

    def quit(self):
        """Overall method to stop and switch off everything.
        """
        self.halt()
        self.off_leds()
        self.off_sounds()
        self.quit_loop()
        self.close()

    def quit_loop(self):
        """Method to quit the main loop.
        """
        pass

    # list of Thymio's properties
    prox_horizontal = property(read_prox_horizontal)
    prox_ground = property(read_prox_ground)
    temperature = property(read_temperature)
    accelerometern = property(read_accelerometer)
    button_center = property(read_button_center)
    button_forward = property(read_button_forward)
    button_backward = property(read_button_backward)
    button_left = property(read_button_left)
    button_right = property(read_button_right)


class ThymioReal(Thymio):

    def __init__(self, world=None):
        if sys.platform == 'linux' or sys.platform == 'linux2':
            self.bridge = 'asebamedulla'
        else:
            self.bridge = 'http'

        super().__init__()
        self._prox_horizontal = [0, 0, 0, 0, 0, 0, 0]
        self._prox_ground_delta = queue.Queue(maxsize=10)
        self._prox_ground_reflected = queue.Queue(maxsize=10)
        self._prox_ground_ambiant = queue.Queue(maxsize=10)
        self._accelerometer = [0, 0, 0]
        self._temperature = 0.0
        self._button_center = 0
        self._button_left = 0
        self._button_right = 0
        self._button_forward = 0
        self._button_backward = 0
        self.init_read()

    def run(self):
        """A method to start the robot.
        You need not call this directly.
        It is called by init_read() method.

        This method calls _run() which is implemented in
        ThymioReal and ThymioSim.
        """
        try:
            self._run()
        except Exception as inst:
            print('Fail running thread.')
            print(type(inst))
            print(inst.args)
            print(inst)
            self.quit()

    def init_read(self):
        """Method to start running the robot in a thread. It calls run().
        """
        self.thread = Thread(target=self.run)
        self.thread.start()

    def open(self):
        self.device = "thymio-II"
        if self.bridge == 'asebamedulla':

            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
            self.bus = dbus.SessionBus()
            self.aseba_proc = subprocess.Popen(['asebamedulla "ser:name=Thymio-II"'],
                                                stdout=subprocess.PIPE, shell=True,
                                                preexec_fn=os.setsid)
            time.sleep(2)
            self.network = dbus.Interface(self.bus.get_object('ch.epfl.mobots.Aseba','/'),
                                          dbus_interface='ch.epfl.mobots.AsebaNetwork')
            node = self.network.GetNodesList()
            progress = 0
            print('connecting: {:d}. \r'.format(progress), end='')
            while node == []:
                self.network = dbus.Interface(self.bus.get_object('ch.epfl.mobots.Aseba','/'),
                                              dbus_interface='ch.epfl.mobots.AsebaNetwork')
                node = self.network.GetNodesList()
                print('connecting: {:d}. \r'.format(progress),
                                 end='', flush=True)
                progress += 1
            print()
            print('connected to {!s:s}.'.format(node))
            self.network.LoadScripts(os.path.dirname(os.path.realpath(__file__)) + 
                                     '/thymiohandlers.aesl')
            self.loop = gobject.MainLoop()
            self.handle = gobject.timeout_add(dt, self.main_loop)
        else:
            #path_to_lib = os.path.dirname(pythymiodw.__file__) + '/' + 'thymiohandlers.aesl'
            #command = ["asebahttp", "--autorestart", "--aesl", path_to_lib, 
            #           "ser:name=Thymio"]
            #self.aseba_proc=subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)    
            time.sleep(2)
            self.httpaddr = 'http://localhost:3000/nodes/'
            r = requests.get(self.httpaddr + self.device)
            json_data = json.loads(r.text)
            node = json_data['name']
            progress = 0
            print('connecting: {:d}. \r'.format(progress), end='')
            while node == []:
                r = requests.get(self.httpaddr + self.device)
                json_data = json.loads(r.text)
                node = json_data['name']
                print('connecting: {:d}. \r'.format(progress),
                                 end='', flush=True)
                progress += 1
            print()
            print('connected to {!s:s}.'.format(node))

    def close(self):
        super().close()
        if self.bridge == 'asebamedulla':
            os.killpg(os.getpgid(self.aseba_proc.pid), signal.SIGTERM)
        # elif sys.platform=='win32':
            # subprocess.call(['taskill','/F','/T','/PID', str(self.aseba_proc.pid)])

    def _run(self):
        try:
            if self.bridge == 'asebamedulla':
                self.loop.run()
        except Exception as e:
            self.quit()

    def get(self, node, var, error_handler):
        try:
            r = requests.get(self.httpaddr + '/' + node + '/' + var)
            data = json.loads(r.text)
            if len(data) == 1:
                return data[0]
            else:
                return data
        except Exception as e:
            error_handler(e)

    def get_ground(self, node, var, reply_handler=None, error_handler=None):
        def get_foo(node, var):
            r = requests.get(self.httpaddr + '/' + node + '/' + var)
            data = json.loads(r.text)
            if len(data) == 1:
                return data[0]
            else:
                return data
        try:
            Thread(target = lambda: reply_handler(get_foo(node, var)) ).start()
        except Exception as e:
            error_handler(e)

    def prox_ground_delta_handler(self, r):
        """Callback for robot to send delta ground proximity sensor data.
        """
        t = [int(x) for x in r]
        self._prox_ground_delta.put(t)

    def prox_ground_ambiant_handler(self, r):
        """Callback for robot to send delta ground proximity sensor data.
        """
        t = [int(x) for x in r]
        self._prox_ambiant_delta.put(t)

    def prox_ground_reflected_handler(self, r):
        """Callback for robot to send delta ground proximity sensor data.
        """
        t = [int(x) for x in r]
        self._prox_reflected_delta.put(t)

    def set(self, node, var, value):
        if self.bridge == 'asebamedulla':
            self.network.SetVariable(node, var, value)
        else:
            post_str = self.httpaddr + '/' + node + '/' + var + '/'
            post_str += '/'.join([str(arg) for arg in value])
            try:
                Thread(target=lambda: requests.post(post_str)).start()
            except Exception as e:
                pass

    def send_event_name(self, event_name, event_args):
        if self.bridge == 'asebamedulla':
            self.network.SendEventName(event_name, event_args,
                                       reply_handler=self.dbus_reply,
                                       error_handler=self.dbus_error)
        else:
            post_str = self.httpaddr + '/' + self.device \
                       + '/' + event_name + '/'
            post_str += '/'.join([str(arg) for arg in event_args])
            try:
                r = requests.post(post_str)
            except Exception as e:
                pass

    def leds_top(self, r=0, g=0, b=0):
        self.send_event_name('SetLEDsTop', [r, g, b])

    def leds_circle(self, led0=0, led1=0, led2=0, led3=0,
                    led4=0, led5=0, led6=0, led7=0):
        self.send_event_name('SetLEDsCircle', [led0, led1, led2,
                                               led3, led4, led5,
                                               led6, led7])

    def leds_buttons(self, led0=0, led1=0, led2=0, led3=0):
        self.send_event_name('SetLEDsButtons', [led0, led1, led2, led3])

    def leds_prox_h(self, led0=0, led1=0, led2=0, led3=0,
                    led4=0, led5=0, led6=0, led7=0):
        self.send_event_name('SetLEDsProxH', [led0, led1, led2,
                                              led3, led4, led5,
                                              led6, led7])

    def leds_prox_v(self, led0=0, led1=0, led2=0, led3=0,
                    led4=0, led5=0, led6=0, led7=0):
        self.send_event_name('SetLEDsProxV', [led0, led1, led2,
                                              led3, led4, led5,
                                              led6, led7])

    def leds_rc(self, led=0):
        self.send_event_name('SetLEDsRC', [led])

    def leds_bottom_left(self, r=0, g=0, b=0):
        self.send_event_name('SetLEDsBottomLeft', [r, g, b])

    def leds_bottom_right(self, r=0, g=0, b=0):
        self.send_event_name('SetLEDsBottomRight', [r, g, b])

    def leds_temperature(self, r=0, b=0):
        self.send_event_name('SetLEDsTemperature', [r, b])

    def leds_sound(self, led=0):
        self.send_event_name('SetLEDsSound', [led])

    def sound_system(self, n=0):
        self.send_event_name('SetSoundSystem', [n])

    def sound_freq(self, hz=0, ds=0):
        self.send_event_name('SetSoundFreq', [hz, ds])

    def sound_play(self, n=0):
        self.send_event_name('SetSoundPlay', [n])

    def sound_replay(self, n=0):
        self.send_event_name('SetSoundReplay', [n])

    def dbus_reply(self):
        pass

    def dbus_error(self, e):
        Thymio.dbus_error(self, e)
        self.quit()

    def sleep(self, n):
        time.sleep(n)

    def prox_horizontal_handler(self, r):
        """Callback for robot to send horizontal proximity sensor data.
        """
        dist = [int(x) for x in r]
        self._prox_horizontal = dist

    def prox_ground_delta_handler(self, r):
        """Callback for robot to send delta ground proximity sensor data.
        """
        t = [int(x) for x in r]
        self._prox_ground_delta = t

    def prox_ground_reflected_handler(self, r):
        """Callback for robot to send reflected ground proximity sensor data.
        """
        t = [int(x) for x in r]
        self._prox_ground_reflected = t

    def prox_ground_ambiant_handler(self, r):
        """Callback for robot to send ambient ground proximity sensor data.
        """
        t = [int(x) for x in r]
        self._prox_ground_ambiant = t

    def acc_handler(self, r):
        """Callback for robot to send accelerometer data.
        """
        t = [int(x) for x in r]
        self._accelerometer = t

    def temperature_handler(self, r):
        """Callback for robot to send temperature sensor data.
        """
        t = [int(x) for x in r]
        self._temperature = t[0] / 10.0

    def button_center_handler(self, r):
        """Callback for robot to send center button press.
        """
        press = [int(x) for x in r]
        self._button_center = press[0]

    def button_left_handler(self, r):
        """Callback for robot to send left button press.
        """
        press = [int(x) for x in r]
        self._button_left = press[0]

    def button_right_handler(self, r):
        """Callback for robot to send right button press.
        """
        press = [int(x) for x in r]
        self._button_right = press[0]

    def button_forward_handler(self, r):
        """Callback for robot to send forward button press.
        """
        press = [int(x) for x in r]
        self._button_forward = press[0]

    def button_backward_handler(self, r):
        """Callback for robot to send backward button press.
        """
        press = [int(x) for x in r]
        self._button_backward = press[0]

    def get_variables_error(self, e):
        super().get_variables_error(e)
        self.quit()

    def get_prox_horizontal(self):
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device,
                                     "prox.horizontal",
                                     reply_handler=self.prox_horizontal_handler,
                                     error_handler=self.get_variables_error)
        else:
            self._prox_horizontal = self.get(self.device,
                                             "prox.horizontal",
                                             error_handler=self.get_variables_error)
        return self._prox_horizontal

    def get_prox_ground_delta(self):
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "prox.ground.delta",
                                     reply_handler=self.prox_ground_delta_handler,
                                     error_handler=self.get_variables_error)
        else:
            self.get_ground(self.device, "prox.ground.delta",
                            reply_handler=self.prox_ground_delta_handler,
                            error_handler=self.get_variables_error)
        return self._prox_ground_delta.get()

    def get_prox_ground_reflected(self):
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "prox.ground.reflected",
                                     reply_handler=self.prox_ground_reflected_handler,
                                     error_handler=self.get_variables_error)
        else:
            self.get_ground(self.device, "prox.ground.reflected",
                            reply_handler=self.prox_ground_reflected_handler,
                            error_handler=self.get_variables_error)
        return self._prox_ground_reflected.get()

    def get_prox_ground_ambiant(self):
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "prox.ground.ambiant",
                                     reply_handler=self.prox_ground_ambiant_handler,
                                     error_handler=self.get_variables_error)
        else:
            self.get_ground(self.device, "prox.ground.ambiant",
                            reply_handler=self.prox_ground_ambiant_handler,
                            error_handler=self.get_variables_error)
        return self._prox_ground_ambiant.get()

    def get_temperature(self):
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "temperature",
                                     reply_handler=self.temperature_handler,
                                     error_handler=self.get_variables_error)
        else:
            self._temperature = self.get(self.device, "temperature",
                                         error_handler=self.get_variables_error)
        return self._temperature

    def get_accelerometer(self):
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "acc",
                                     reply_handler=self.acc_handler,
                                     error_handler=self.get_variables_error)
        else:
            self._accelerometer = self.get(self.device, "acc",
                                           error_handler=self.get_variables_error)
        return self._accelerometer

    def get_button_center(self):
        """Method to get center button.
        """
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "button.center",
                                     reply_handler=self.button_center_handler,
                                     error_handler=self.get_variables_error)
        else:
            self._button_center = self.get(self.device, "button.center",
                                           error_handler=self.get_variables_error)
        return self._button_center

    def get_button_left(self):
        """Method to get left button.
        """
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "button.left",
                                     reply_handler=self.button_left_handler,
                                     error_handler=self.get_variables_error)
        else:
            self._button_left = self.get(self.device, "button.left",
                                         error_handler=self.get_variables_error)
        return self._button_left

    def get_button_right(self):
        """Method to get right button.
        """
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "button.right",
                                     reply_handler=self.button_right_handler,
                                     error_handler=self.get_variables_error)
        else:
            self._button_right = self.get(self.device, "button.right",
                                          error_handler=self.get_variables_error)
        return self._button_right

    def get_button_forward(self):
        """Method to get forward button.
        """
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "button.forward",
                                     reply_handler=self.button_forward_handler,
                                     error_handler=self.get_variables_error)
        else:
            self._button_forward = self.get(self.device, "button.forward",
                                            error_handler=self.get_variables_error)
        return self._button_forward

    def get_button_backward(self):
        """Method to get backward button.
        """
        if self.bridge == 'asebamedulla':
            self.network.GetVariable(self.device, "button.backward",
                                     reply_handler=self.button_backward_handler,
                                     error_handler=self.get_variables_error)
        else:
            self._button_backward = self.get(self.device, "button.backward",
                                             error_handler=self.get_variables_error)
        return self._button_backward

    def _wheels(self, l, r):
        self.set(self.device, "motor.left.target", [l])
        self.set(self.device, "motor.right.target", [r])

    def _halt(self):
        self.set(self.device, "motor.left.target", [0])
        self.set(self.device, "motor.right.target", [0])

    def quit_loop(self):
        if self.bridge == 'asebamedulla':
            self.loop.quit()

    def read_prox_ground(self):
        self.get_prox_ground_delta()
        self.get_prox_ground_reflected()
        self.get_prox_ground_ambiant()
        return io.ProxGround(delta=self._prox_ground_delta,
                             reflected=self._prox_ground_reflected,
                             ambiant=self._prox_ground_ambiant)

    prox_horizontal = property(get_prox_horizontal)
    prox_ground = property(read_prox_ground)
    temperature = property(get_temperature)
    accelerometer = property(get_accelerometer)
    button_center = property(get_button_center)
    button_forward = property(get_button_forward)
    button_backward = property(get_button_backward)
    button_left = property(get_button_left)
    button_right = property(get_button_right)


class ThymioSim(Thymio):

    def __init__(self, world=None, scale=1):
        if sys.platform != 'darwin':
            Thread(target=self.run_iowindow, name='IO Window').start()
        super().__init__()
        self.forward_velocity = 0.0
        self.rotational_velocity = 0.0
        self.leftv = 0
        self.rightv = 0
        self.heading = 0.0
        self.world = world
        self.scale = scale
        if self.world is not None:
            ll, ur = self.world.get_world_boundaries()
            self.window.setworldcoordinates(ll.x, ll.y, ur.x, ur.y)
            self.world.draw_world(self.robot, self.scale)
            init_pos = self.world.get_init_pos()
            self.init_pos = Point(init_pos.x * self.scale,
                                  init_pos.y * self.scale)
            self.heading = self.world.get_init_heading()
        else:
            pos = self.robot.position()
            self.init_pos = Point(pos[0], pos[1])
            self.heading = 0
        self.robot.setposition(self.init_pos.x, self.init_pos.y)
        self.robot.setheading(self.heading)
        self._button_center = 0
        self._button_forward = 0
        self._button_backward = 0
        self._button_left = 0
        self._button_right = 0

    def open(self):
        self.window = turtle.Screen()
        self.robot = turtle.Turtle()

    def run(self):
        self.get_prox_horizontal()
        self.get_prox_ground()
        self.get_temperature()
        self._wheels(self.leftv, self.rightv)

    def quit(self):
        self.tk.quit()
        super().quit()

    def button_pressed(self, val):
        if val == 'forward':
            self._button_forward = 1
        elif val == 'left':
            self._button_left = 1
        elif val == 'right':
            self._button_right = 1
        elif val == 'backward':
            self._button_backward = 1
        elif val == 'center':
            self._button_center = 1

    def run_iowindow(self):
        self.tk = tk.Tk()
        self.canvas = tk.Canvas(self.tk, width=300, height=300)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        script_dir = os.path.dirname(__file__)
        rel_path = 'images/iodisplay.png'
        abs_file_path = os.path.join(script_dir, rel_path)
        tk_img = ImageTk.PhotoImage(file=abs_file_path)
        self.canvas.create_image(150, 150, image=tk_img)
        self.led = self.canvas.create_rectangle(100, 175, 200, 250,
                                                fill='#000000')
        button_forward = tk.Button(self.tk, text='forward',
                                   command=lambda: self.button_pressed('forward'),
                                   width=7)
        button_left = tk.Button(self.tk, text='left',
                                command=lambda: self.button_pressed('left'),
                                width=7)
        button_right = tk.Button(self.tk, text='right',
                                 command=lambda: self.button_pressed('right'),
                                 width=7)
        button_backward = tk.Button(self.tk, text='backward',
                                    command=lambda: self.button_pressed('backward'),
                                    width=7)
        button_center = tk.Button(self.tk, text='center',
                                  command=lambda: self.button_pressed('center'),
                                  width=7)

        button_forward.place(x=120, y=30)
        button_left.place(x=40, y=90)
        button_right.place(x=200, y=90)
        button_backward.place(x=120, y=150)
        button_center.place(x=120, y=90)
        self.tk.mainloop()

    def leds_top(self, r=0, g=0, b=0):
        if sys.platform != 'darwin':
            self.canvas.itemconfig(self.led, fill=self.colorconvert(r, g, b))

    def colorconvert(self, r, g, b):
        # conversion to 255
        r = int(r * 7.9687)
        g = int(g * 7.9687)
        b = int(b * 7.9687)
        # conversion to hex
        dectohex = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
                    6: 6, 7: 7, 8: 8, 9: 9, 10: 'A',
                    11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
        first = dectohex[r // 16]
        second = dectohex[r % 16]
        third = dectohex[g // 16]
        fourth = dectohex[g % 16]
        fifth = dectohex[b // 16]
        sixth = dectohex[b % 16]
        hexcode = '#{}{}{}{}{}{}'.format(first, second, third,
                                         fourth, fifth, sixth)
        return hexcode

    def wheels(self, l, r):
        self.leftv = l
        self.rightv = r

    def speed_to_pixel(self, l, r):
        # 20cm/s divided by max speed wheels 500
        vl = 20 / 500.0 * l * dt / 1000
        vr = 20 / 500.0 * r * dt / 1000
        return vl, vr

    def sleep(self, n):
        t = 0
        while t < n:
            self.run()
            t += dt / 1000
            time.sleep(dt / 1000)

    def rad_to_deg(self, omega):
        return omega / math.pi * 180

    def _wheels(self, l, r):
        W = 0.095 * 100
        vl, vr = self.speed_to_pixel(l, r)
        omega = 1 / W * (vr - vl)
        omegadeg = self.rad_to_deg(omega)
        fv = 0.5 * (vr + vl)
        self.heading += omegadeg
        can_move = self.check_world(fv)
        if can_move:
            self.robot.forward(fv)
        self.robot.setheading(self.heading)

    def check_world(self, fv):
        if self.world is None:
            return True
        rad = fv * dt / 1000.0 * self.scale
        new_x, new_y = self.get_new_point(rad)
        if self.world.is_overlap(Point(new_x, new_y), self.scale):
            return False
        ll, ur = self.world.get_world_boundaries()
        if new_x < ll.x * self.scale or new_x > ur.x * self.scale \
           or new_y < ll.y * self.scale or new_y > ur.y * self.scale:
            return False
        return True

    def get_new_point(self, rad):
        angle = self.robot.heading()
        angle_rad = angle / 180.0 * math.pi
        x, y = self.robot.position()
        dx = rad * math.cos(angle_rad) * self.scale
        dy = rad * math.sin(angle_rad) * self.scale
        new_x, new_y = x + dx, y + dy
        return new_x, new_y

    def get_prox_horizontal(self):
        rad = 10  # when it is 10cm
        new_x, new_y = self.get_new_point(rad)
        self._prox_horizontal = [0 for i in range(7)]
        if self.world is not None:
            if self.world.is_overlap(Point(new_x, new_y)):
                self._prox_horizontal[2] = 1000
        return self._prox_horizontal

    def get_prox_ground(self):
        posx, posy = self.robot.position()
        delta = 500
        leftx = posx - 1
        rightx = posx + 1
        lefty = righty = posy
        self._prox_ground_delta = [0, 0]
        self._prox_ground_reflected = [1000, 1000]
        self._prox_ground_ambiant = [1000, 1000]
        if self.world is not None:
            if self.world.is_overlap(Point(leftx, lefty)):
                self._prox_ground_reflected[0] = self._prox_ground_ambiant[0] - delta
            else:
                self._prox_ground_reflected[0] = self._prox_ground_ambiant[0]

            if self.world.is_overlap(Point(rightx, righty)):
                self._prox_ground_reflected[1] = self._prox_ground_ambiant[1] - delta
            else:
                self._prox_ground_reflected[1] = self._prox_ground_ambiant[1]
        self._prox_ground_delta[0] = self._prox_ground_ambiant[0] - self._prox_ground_reflected[0]
        self._prox_ground_delta[1] = self._prox_ground_ambiant[1] - self._prox_ground_reflected[1]
        return io.ProxGround(delta=self._prox_ground_delta,
                             reflected=self._prox_ground_reflected,
                             ambiant=self._prox_ground_ambiant)


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ThymioSim3D(Thymio):

    def __init__(self, init_pos=(100, 100), heading=0):
        super().__init__()
        self.leftv = 0
        self.rightv = 0
        self.heading = heading
        self.init_pos = init_pos

    def open(self):
        self.device = "thymio-II"

    def close(self):
        Thymio.close(self)

    def run(self):
        self.get_prox_horizontal()
        self.get_prox_ground()
        self.get_temperature()
        self._wheels(self.leftv, self.rightv)

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, val):
        val = val % 360
        self._heading = val

    @property
    def init_pos(self):
        return self._init_pos

    @init_pos.setter
    def init_pos(self, val):
        if len(val) < 2:
            self._init_pos = (100, 100)
        if val[0] < 0:
            x = 100
        else:
            x = val[0]
        if val[1] < 0:
            y = 100
        else:
            y = val[1]
        self._init_pos = (x, y)

    @property
    def leftv(self):
        return self._leftv

    @leftv.setter
    def leftv(self, val):
        self._leftv = val

    @property
    def rightv(self):
        return self._rightv

    @rightv.setter
    def rightv(self, val):
        self._rightv = val

    def wheels(self, l, r):
        self._leftv = int(l)
        self._rightv = int(r)

    @property
    def prox_horizontal(self):
        return self._prox_horizontal

    @prox_horizontal.setter
    def prox_horizontal(self, val_list):
        self._prox_horizontal = val_list

    @property
    def prox_ground(self):
        return (self._prox_ground_delta,
                self._prox_ground_ambiant,
                self._prox_ground_reflected)

    @prox_ground.setter
    def prox_ground(self, values):
        self._prox_ground_delta = values[0]
        self._prox_ground_ambiant = values[1]
        self._prox_ground_reflected = values[2]

    def quit(self):
        super().quit()


class ThymioSimPG(ThymioSim):

    def __init__(self, world=None, scale=1):
        pygame.init()
        self.scale = scale
        super().__init__(world, scale)

    def open(self):
        self.window = PGWindow(scale=self.scale)
        self.robot = PGRobot(self.window, scale=self.scale)

    def run(self):
        super().run()
        self.window.screen.fill(self.window.color)
        if self.world is not None:
            self.world.draw_world(self.robot, self.scale)

    def sleep(self, n):
        t = 0
        while t < n:
            self.run()
            t += dt / 1000
            time.sleep(dt / 1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            self.run()
            t += dt / 1000
            time.sleep(dt / 1000)

    def get_new_point(self, rad):
        angle = self.robot.heading()
        angle_rad = angle / 180.0 * math.pi
        x, y = self.robot.position()
        rect = self.robot._image.get_rect()
        x = x + rect.center[0] * math.cos(angle_rad)
        y = y + rect.center[1] * math.sin(angle_rad)
        dx = rad * math.cos(angle_rad) * self.scale
        dy = rad * math.sin(angle_rad) * self.scale
        new_x, new_y = x + dx, y - dy
        return new_x, new_y

    def get_prox_horizontal(self):
        self._prox_horizontal = [0 for i in range(7)]
        if self.world is not None:
            prox_horizontal = self.robot.get_horizontal_sensor_position()
            range_horizontal = self.robot.get_range_points_of_sensor()
            dic = {}
            for i in range(7):
                dic[i] = Line(Point(prox_horizontal[i][0] / self.scale,
                                    prox_horizontal[i][1] / self.scale),
                              Point(range_horizontal[i][0] / self.scale,
                                    range_horizontal[i][1] / self.scale))
            distances = [-1 for i in range(7)]
            for block in self.world.blocks:
                if isinstance(block, Floor):
                    continue
                for i in range(7):
                    intersect_point = block.is_line_intersect(dic[i],
                                                              self.scale)
                    if intersect_point is not False:
                        point_xy, dist_min = intersect_point
                        distances[i] = dist_min / self.scale
            for i in range(7):
                if distances[i] == -1:
                    self._prox_horizontal[i] = 0
                else:
                    A = 4.76569216e5
                    B = 4.14625464
                    C = 9.6766127e1
                    reading = A / (distances[i] * distances[i] +
                                   B * distances[i] + C)
                    self._prox_horizontal[i] = reading

        return self._prox_horizontal

    def check_floor(self):
        left = None
        right = None
        left_pos, right_pos = self.robot.get_ground_sensor_position()
        if self.world is not None:
            for block in self.world.blocks:
                if block.is_overlap(Point(left_pos[0], left_pos[1]),
                                    self.scale):
                    left = block
                if block.is_overlap(Point(right_pos[0], right_pos[1]),
                                    self.scale):
                    right = block
        return left, right

    def get_prox_ground(self):
        left, right = self.check_floor()
        delta = [1023, 1023]
        ambiant = [0, 0]
        if isinstance(left, Floor):
            color = left.color
            color_average = (color[0] + color[1] + color[2]) / 3
            delta[0] = (int(1023 * color_average / 255))
        if isinstance(right, Floor):
            color = right.color
            color_average = (color[0] + color[1] + color[2]) / 3
            delta[1] = (int(1023 * color_average / 255))
        self._prox_ground_delta = delta
        self._prox_ground_reflected = delta
        self._prox_ground_ambiant = ambiant
        return io.ProxGround(delta=self._prox_ground_delta,
                             reflected=self._prox_ground_reflected,
                             ambiant=self._prox_ground_ambiant)
