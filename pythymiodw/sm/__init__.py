from .. import *
from ..io import Input
import time
from threading import Thread, Event
import sys

class ThymioSMSim():
    def __init__(self,MySM,world=None):
        global base_class
        base_class=ThymioSim
        self.thymio=ThymioSM2(MySM,world)
    
    def start(self):
        try:
            while True:
                if not self.thymio.behaviour.done(self.thymio.behaviour.state):
                    self.thymio.update()
                else:
                    self.stop()
                    break
                self.thymio.sleep(dt/1000.0)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print('Error:',e)
            self.stop()

    def stop(self):
        self.thymio.quit()
        sys.exit(1)

class ThymioSMReal(Thread):
    def __init__(self, MySM,world=None):
        global base_class
        base_class=ThymioReal
        Thread.__init__(self)
        self.thymio=ThymioSM1(MySM)
        self.stopped=Event()

    def run(self):
        while not self.stopped.wait(dt/1000.0):
            try: 
                if not self.thymio.behaviour.done(self.thymio.behaviour.state):
                    self.thymio.update()
                else:
                    self.stop()
            except Exception as e:
                print('Error:',e)
                self.stop()

    def stop(self):
        self.stopped.set()
        self.thymio.quit()

class ThymioSM1(ThymioReal):
    def __init__(self,MySM):
        base_class.__init__(self)
        self.behaviour=MySM
        self.input=Input()
        self.behaviour.start()
        self.init_read()

    def update(self):
        self.input.prox_horizontal=self.prox_horizontal
        self.input.prox_ground=self.prox_ground
        self.input.temperature=self.temperature
        self.input.accelerometer=self.accelerometer
        self.input.button_center=self.button_center
        self.input.button_left=self.button_left
        self.input.button_right=self.button_right
        self.input.button_forward=self.button_forward
        self.input.button_backward=self.button_backward
        output=self.behaviour.step(self.input)
        self.move(output)
            
    def move(self, output):
        self.wheels(output.leftv,output.rightv)

class ThymioSM2(ThymioSim):
    def __init__(self,MySM,world):
        base_class.__init__(self,world)
        self.behaviour=MySM
        self.input=Input()
        self.behaviour.start()

    def update(self):
        self.input.prox_horizontal=self.prox_horizontal
        self.input.prox_ground=self.prox_ground
        self.input.temperature=self.temperature
        #self.input.accelerometer=self.accelerometer
        #self.input.button_center=self.button_center
        #self.input.button_left=self.button_left
        #self.input.button_right=self.button_right
        #self.input.button_forward=self.button_forward
        #self.input.button_backward=self.button_backward
        output=self.behaviour.step(self.input)
        self.move(output)
            
    def move(self, output):
        self.wheels(output.leftv,output.rightv)

