import os
import Pyro4
import subprocess
import signal
from pythymiodw import ThymioSimMR


class ThymioMR():
	def __init__(self):
		self.pyro4daemon_proc=subprocess.Popen(['python -m pythymiodw.pyro.__main__'], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)    
		self.robot = Pyro4.Proxy('PYRONAME:pythymiodw.thymiosimmr')

	def quit(self):
		self.robot.quit()
		os.killpg(os.getpgid(self.pyro4daemon_proc.pid), signal.SIGTERM)        

	def wheels(self, lv, rv):
		self.robot.wheels(lv, rv)

	def get_wheels(self):
		return self.robot.leftv, self.robot.rightv

        
