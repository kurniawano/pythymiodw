from __future__ import print_function
import sys
#sys.path.append('..')

from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm


class TestRead(sm.SM):
    def get_next_values(self,state, inp):
        	print(inp.prox_horizontal[2])
        	print(inp.prox_ground.delta)
        	#print inp.temperature
        	#print inp.accelerometer
        	return state, io.Action(fv=0.00,rv=0)
	
MySM=TestRead()

############################

set_base(ThymioReal)
m=ThymioSM(MySM)
try:
    m.run()
except:
    m.quit()
