from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm
import time


class TestRead(sm.SM):

    start_state = 0

    def get_next_values(self, state, inp):
        # if inp.button_backward:
        #    return 'halt', io.Action(0,0)
        print(inp.prox_horizontal[2])
        # print(inp.prox_ground.delta)
        # print inp.temperature
        # print inp.accelerometer
        if inp.prox_horizontal[2] > 10000:
            state = 'halt'
            forward = 0.0
        else:
            forward = state + 0.1
            state = forward
        return state, io.Action(fv=forward, rv=0)

    def done(self, state):
        if state == 'halt':
            return True
        else:
            return False


MySM = TestRead()

############################

# m=ThymioSMSim(MySM,thymio_world)
m = ThymioSMSim(MySM, graphic='3D')
try:
    print('Run C# code now.')
    time.sleep(5)
    m.start()
except KeyboardInterrupt:
    m.stop()
