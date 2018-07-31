import os
import sys
import Pyro4
import subprocess
import signal
from pythymiodw import ThymioSimMR
import time
from pythymiodw.io import ProxGround


class ThymioMR():
	def __init__(self):
		if sys.platform == 'win32':
			self.pyro4daemon_proc=subprocess.Popen([sys.executable,'-m', 'pythymiodw.pyro.__main__'], stdout=subprocess.PIPE, shell=True)
		else:
			self.pyro4daemon_proc=subprocess.Popen(['python -m pythymiodw.pyro.__main__'], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)    

		time.sleep(2)
		self.robot = Pyro4.Proxy('PYRONAME:pythymiodw.thymiosimmr')

	def quit(self):
		self.robot.quit()
		if sys.platform == 'win32':
			subprocess.call(['taskkill','/F','/T','/PID',str(self.pyro4daemon_proc.pid)])
		else:
			os.killpg(os.getpgid(self.pyro4daemon_proc.pid), signal.SIGTERM)        


	def wheels(self, lv, rv):
		self.robot.wheels(lv, rv)

	def get_wheels(self):
		return self.robot.leftv, self.robot.rightv

	def sleep(self, sec):
		time.sleep(sec)

	@property
	def prox_horizontal(self):
		return self.robot.prox_horizontal

	@property
	def prox_ground(self):
		delta, ambiant, reflected = self.robot.prox_ground
		return ProxGround(delta, ambiant, reflected)
	
	

        
