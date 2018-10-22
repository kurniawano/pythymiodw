from .. import *
from ..io import Input
from ..pyro import Thymio3D
from threading import Thread, Event
import sys


class ThymioSMSim():

    def __init__(self, MySM, world=None, graphic='pygame', scale=1):
        if graphic == 'pygame':
            self.thymio = ThymioSMPG(MySM, world, scale)
        elif graphic == 'turtle':
            self.thymio = ThymioSMTurtle(MySM, world, scale)
        elif graphic == '3D':
            self.thymio = ThymioSM3DBase(MySM)

    def start(self):
        try:
            while True:
                if not self.thymio.behaviour.done(self.thymio.behaviour.state):
                    self.thymio.update()
                else:
                    self.stop()
                    break
                self.thymio.sleep(dt / 1000.0)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print('Error:', e)
            self.stop()

    def stop(self):
        self.thymio.quit()
        sys.exit(1)


class ThymioSMReal(Thread):

    def __init__(self, MySM, world=None):
        super().__init__()
        self.thymio = ThymioSM1(MySM)
        self.stopped = Event()

    def run(self):
        while not self.stopped.wait(dt / 1000.0):
            try:
                if not self.thymio.behaviour.done(self.thymio.behaviour.state):
                    self.thymio.update()
                else:
                    self.stop()
            except Exception as e:
                print('Error:', e)
                self.stop()

    def stop(self):
        self.stopped.set()
        self.thymio.quit()


class ThymioSM3D():

    def __init__(self, MySM):
        self.thymio = ThymioSM3DBase(MySM)

    def start(self):
        try:
            while True:
                if not self.thymio.behaviour.done(self.thymio.behaviour.state):
                    self.thymio.update()
                else:
                    self.stop()
                    break
                self.thymio.sleep(dt / 1000.0)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print('Error:', e)
            self.stop()

    def stop(self):
        self.thymio.quit()
        sys.exit(1)


class ThymioSM1(ThymioReal):

    def __init__(self, MySM):
        super().__init__(self)
        self.behaviour = MySM
        self.input = Input()
        self.behaviour.start()
        self.init_read()

    def update(self):
        self.input.prox_horizontal = self.prox_horizontal
        self.input.prox_ground = self.prox_ground
        self.input.temperature = self.temperature
        self.input.accelerometer = self.accelerometer
        self.input.button_center = self.button_center
        self.input.button_left = self.button_left
        self.input.button_right = self.button_right
        self.input.button_forward = self.button_forward
        self.input.button_backward = self.button_backward
        output = self.behaviour.step(self.input)
        self.move(output)

    def move(self, output):
        self.wheels(output.leftv, output.rightv)


class ThymioSMSimBase:

    def __init__(self, *args, **kwargs):
        MySM = args[0]
        if len(args) > 1:
            world = args[1]
            scale = args[2]
            super().__init__(world, scale)
        else:
            super().__init__()
        self.behaviour = MySM
        self.input = Input()
        self.behaviour.start()

    def update(self):
        self.input.prox_horizontal = self.prox_horizontal
        self.input.prox_ground = self.prox_ground
        self.input.temperature = self.temperature
        # self.input.accelerometer=self.accelerometer
        # self.input.button_center=self.button_center
        # self.input.button_left=self.button_left
        # self.input.button_right=self.button_right
        # self.input.button_forward=self.button_forward
        # self.input.button_backward=self.button_backward
        output = self.behaviour.step(self.input)
        self.move(output)

    def move(self, output):
        self.wheels(output.leftv, output.rightv)


class ThymioSMTurtle(ThymioSMSimBase, ThymioSim):

    pass


class ThymioSMPG(ThymioSMSimBase, ThymioSimPG):

    pass


class ThymioSM3DBase(ThymioSMSimBase, Thymio3D):

    def update(self):
        self.input.prox_horizontal = self.prox_horizontal
        self.input.prox_ground = self.prox_ground
        # self.input.temperature = self.temperature
        # self.input.accelerometer=self.accelerometer
        # self.input.button_center=self.button_center
        # self.input.button_left=self.button_left
        # self.input.button_right=self.button_right
        # self.input.button_forward=self.button_forward
        # self.input.button_backward=self.button_backward
        output = self.behaviour.step(self.input)
        self.move(output)
