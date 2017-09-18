from __future__ import print_function
import sys
#sys.path.append('..')

from pythymiodw import io
from pythymiodw.sm import ThymioSM
from libdw import sm


class TestRead(sm.SM):
    def getNextValues(self,state, inp):
	print('Delta:',inp.prox_ground.delta)
	print('Reflected:',inp.prox_ground.reflected)
	print('Ambient:',inp.prox_ground.ambiant)
	return state, io.Action(fv=0.00,rv=0)
	
MySM=TestRead()

############################

m=ThymioSM(MySM)
try:
    m.run()
except:
    m.quit()
