from __future__ import print_function
import sys
#sys.path.append('..')

from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm


class TestRead(sm.SM):
    start_state='move'
    def get_next_values(self,state, inp):
       	print(inp.prox_horizontal[2])
       	print(inp.prox_ground.delta)
       	#print inp.temperature
       	#print inp.accelerometer
        if inp.prox_horizontal[2]>0:
            state='done'
            forward=0.0
        else:
            forward=0.1
        return state, io.Action(fv=forward,rv=0)
	
    def done(self,state):
        if state=='done':
            return True
        else:
            return False

MySM=TestRead()

############################

set_base(ThymioReal)
m=ThymioSM(MySM)
try:
    m.start()
   # m.run()
except KeyboardInterrupt:
    m.stop()
