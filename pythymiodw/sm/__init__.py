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
	Thymio.__init__(self)
	self.behaviour=MySM
	self.behaviour.start()
	self.input=Input()

    def main_loop(self):
	prox_data=self.get_prox_sensors_val()
	temp_data=self.get_temperature()
	acc_data=self.get_accelerometer()
	self.input.proximity=copy.deepcopy(prox_data)
	self.input.temperature=copy.deepcopy(temp_data)
	self.input.accelerometer=copy.deepcopy(acc_data)
	output=self.behaviour.step(self.input)
	self.move(output)
	return True

    def move(self, output):
	self.wheels(output.leftv,output.rightv)

