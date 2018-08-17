from pythymiodw import ThymioSimPG
from pgworld import *

robot=ThymioSimPG(thymio_world, scale = 3)
robot.sleep(1)
print('move')
robot.wheels(200,200)
count = 0
while count < 15:
	#print(robot.heading)
	print(robot.robot._position)
	robot.sleep(1)
	count += 1

print('stop')
robot.wheels(0,0)
robot.quit()