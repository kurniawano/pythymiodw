from pythymiodw import *
from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm
from pgboxworld import *


class MySMClass(sm.SM):

    start_state = None

    def get_next_values(self, state, inp):
        ground = inp.prox_ground.delta
        left = ground[0]
        right = ground[1]
        print(left, right)
        # print(inp.prox_ground.delta)
        # print(inp.prox_ground.reflected)
        # print(inp.prox_ground.ambiant)
        return state, io.Action(fv=0.05, rv=0.1)


MySM = MySMClass()

############################

m = ThymioSMSim(MySM, thymio_world, scale=3)
try:
    m.start()
except KeyboardInterrupt:
    m.stop()
