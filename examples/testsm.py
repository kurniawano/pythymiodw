from pythymiodw import io
from pythymiodw.env import ThymioPhysical
from libdw import sm


class TestRead(sm.SM):
    def getNextValues(self,state, inp):
	print inp
	return state, io.Action(10,0)
	
MySM=TestRead()

############################

m=ThymioPhysical(MySM)
try:
    m.run()
except:
    m.quit()
