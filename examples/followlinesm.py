from pythymiodw import *
from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm

class FollowLine(sm.SM):
    start_state='find'
    def done(self,state):
        if state=='halt':
            return True
        else:
            return False

    def get_next_values(self, state, inp):
        if inp.button_backward:
            return 'halt', io.Action(0,0)

        ground=inp.prox_ground.delta
        left=ground[0]
        right=ground[1]
        diff=left-right
        print(state)
        print(left, right, diff)
        if state=='follow':
            if diff>500:
                fv=0.05
                rv=0.0
            elif diff<-500:
                fv=0.05
                rv=0.2
            elif -100<diff<100 and  left>500 and right>500:
                fv=0.01
                rv=-0.2
            elif  -100<diff<100 and left<500 and right<500:
                fv=0
                rv=0.2
            else:
                fv=0.05
                rv=0.0
            next_state='follow'
        elif state=='find':
            if -100<diff<100 and 0<left<500 and 0<right<500:
                fv=0.0
                rv=0.2
                next_state='follow'
            else:
                fv=0.05
                rv=0.0
                next_state='find'
            
                    
        return next_state, io.Action(fv, rv)

MySM=FollowLine()

############################

m=ThymioSMReal(MySM)
try:
    m.start()
except KeyboardInterrupt:
    m.stop()
