from __future__ import print_function
import sys
#sys.path.append('..')

from pythymiodw import io
from pythymiodw.sm import ThymioSMReal
from libdw import sm


class TestRead(sm.SM):
    def get_next_values(self,state, inp):
        print('Delta:',inp.prox_ground.delta)
        print('Reflected:',inp.prox_ground.reflected)
        print('Ambient:',inp.prox_ground.ambiant)
        return state, io.Action(fv=0.00,rv=0)
    
MySM=TestRead()

############################

m=ThymioSMReal(MySM)
try:
    m.start()
except:
    m.quit()
