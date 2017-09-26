class Action(object):
    leftv=0
    rightv=0
    fv=0
    rv=0
    W=0.095

    
    def __init__(self, fv=0.0, rv=0.0):
        self.fv=fv
        self.rv=rv
        self.convert()

    def convert(self):
        self.leftv=self.fv-0.5*self.W*self.rv
        self.leftv=(500/0.2)*self.leftv
        self.rightv=self.fv+0.5*self.W*self.rv
        self.rightv=(500/0.2)*self.rightv

class Input(object):
    def __init__(self):
        self.prox_horizontal=[0.0 for i in range(7)]
        self.prox_ground=ProxGround()
        self.temperature=0.0
        self.accelerometer=[0.0,0.0,0.0]

class ProxGround(object):
    def __init__(self,delta=[0.0,0.0],reflected=[0.0,0.0],ambiant=[0.0,0.0]):
        self.delta=delta
        self.reflected=reflected
        self.ambiant=ambiant
