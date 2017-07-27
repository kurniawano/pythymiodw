from .. import Thymio

class ThymioPhysical(Thymio):
    def __init__(self,MySM):
	Thymio.__init__(self)
	self.behaviour=MySM
	self.behaviour.start()

    def main_loop(self):
	prox_data=self.get_prox_sensors_val()
	output=self.behaviour.step(prox_data)
	self.wheels(output.lv,output.rv)
	return True
