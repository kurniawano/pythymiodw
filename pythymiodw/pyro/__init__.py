import os
import sys
import Pyro4
import subprocess
import signal
import time
from pythymiodw.io import ProxGround


class Thymio3D():

    def __init__(self, init_pos=(100, 100), heading=0):
        if sys.platform == 'win32':
            self.pyro4ns_proc = subprocess.Popen(['pyro4-ns'],
                                                 stdout=subprocess.PIPE,
                                                 shell=True)
            time.sleep(2)
            self.pyro4daemon_proc = subprocess.Popen([sys.executable,
                                                      '-m','pythymiodw.pyro.__main__'],
                                                     stdout=subprocess.PIPE,
                                                     shell=True)

        else:
            self.pyro4ns_proc = subprocess.Popen(['pyro4-ns'],
                                                 stdout=subprocess.PIPE,
                                                 shell=True,
                                                 preexec_fn=os.setsid)
            time.sleep(2)
            self.pyro4daemon_proc = subprocess.Popen(['python -m pythymiodw.pyro.__main__'],
                                                      stdout=subprocess.PIPE,
                                                      shell=True,
                                                      preexec_fn=os.setsid)
        time.sleep(2)
        self.robot = Pyro4.Proxy('PYRONAME:pythymiodw.thymiosim3d')

    def quit(self):
        self.robot.quit()
        if sys.platform == 'win32':
            subprocess.call(['taskkill', '/F', '/T',
                             '/PID', str(self.pyro4daemon_proc.pid)])
            subprocess.call(['taskkill', '/F', '/T',
                             '/PID', str(self.pyro4ns_proc.pid)])
        else:
            os.killpg(os.getpgid(self.pyro4daemon_proc.pid),
                      signal.SIGTERM)
            os.killpg(os.getpgid(self.pyro4ns_proc.pid),
                      signal.SIGTERM)

    def wheels(self, lv, rv):
        self.robot.wheels(lv, rv)

    def get_wheels(self):
        return self.robot.leftv, self.robot.rightv

    def sleep(self, sec):
        try:
          time.sleep(sec)
        except KeyboardInterrupt:
          self.quit()

    @property
    def prox_horizontal(self):
        return self.robot.prox_horizontal

    @property
    def prox_ground(self):
        delta, ambiant, reflected = self.robot.prox_ground
        return ProxGround(delta, ambiant, reflected)

    @property
    def init_pos(self):
        return self.robot.init_pos

    @init_pos.setter
    def init_pos(self, val):
        self.robot.init_pos = val

    @property
    def heading(self):
        return self.robot.heading

    @heading.setter
    def heading(self, val):
        self.robot.heading = val
