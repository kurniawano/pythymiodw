import os
import sys
import Pyro4
import subprocess
import signal
from pythymiodw import ThymioSim3D
import time
from pythymiodw.io import ProxGround


class Thymio3D():
	def __init__(self):
		if sys.platform == 'win32':
			self.pyro4ns_proc=subprocess.Popen(['pyro4-ns'], stdout=subprocess.PIPE, shell=True)			
			time.sleep(2)			
			self.pyro4daemon_proc=subprocess.Popen([sys.executable,'-m', 'pythymiodw.pyro.__main__'], stdout=subprocess.PIPE, shell=True)

		else:
			self.pyro4ns_proc=subprocess.Popen(['pyro4-ns'], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)    
			time.sleep(2)
			self.pyro4daemon_proc=subprocess.Popen(['python -m pythymiodw.pyro.__main__'], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)    
		time.sleep(2)
		self.robot = Pyro4.Proxy('PYRONAME:pythymiodw.thymiosim3d')

	def quit(self):
		self.robot.quit()
		if sys.platform == 'win32':
			subprocess.call(['taskkill','/F','/T','/PID',str(self.pyro4daemon_proc.pid)])
			subprocess.call(['taskkill','/F','/T','/PID',str(self.pyro4ns_proc.pid)])
		else:
			os.killpg(os.getpgid(self.pyro4daemon_proc.pid), signal.SIGTERM)        
			os.killpg(os.getpgid(self.pyro4ns_proc.pid), signal.SIGTERM)        


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
	
	

        
