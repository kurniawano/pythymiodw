from .. import Thymio
from ..io import Input
import copy


class ThymioEnv(Thymio):
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
    def move(self,output):
	pass

class ThymioPhysical(ThymioEnv):
    def move(self, output):
	self.wheels(output.leftv,output.rightv)

