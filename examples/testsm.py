import sys
sys.path.append('..')

from pythymiodw import io
from pythymiodw.env import ThymioPhysical
from libdw import sm


class TestRead(sm.SM):
    def getNextValues(self,state, inp):
	print inp.proximity[2]
	#print inp.temperature
	#print inp.accelerometer
	return state, io.Action(fv=0.05,rv=0)
	
MySM=TestRead()

############################

m=ThymioPhysical(MySM)
try:
    m.run()
except:
    m.quit()
