from .. import *
from ..io import Input
import copy

base_class = ThymioReal

def set_base(base=ThymioReal):
    global base_class 
    base_class = base

def set_base_simulator():
    set_base(ThymioSim)

class ThymioSM(base_class):
    def __init__(self,MySM):
        base_class.__init__(self)
        self.behaviour=MySM
        self.behaviour.start()
        self.input=Input()

    def main_loop(self):
        prox_horizontal=self.get_prox_horizontal()
        prox_ground=self.get_prox_ground()
        temperature=self.get_temperature()
        accelerometer=self.get_accelerometer()
        self.input.prox_horizontal=copy.deepcopy(prox_horizontal)
        self.input.prox_ground=copy.deepcopy(prox_ground)
        self.input.temperature=copy.deepcopy(temperature)
        self.input.accelerometer=copy.deepcopy(accelerometer)
        output=self.behaviour.step(self.input)
        self.move(output)
        return True

    def move(self, output):
        self.wheels(output.leftv,output.rightv)

