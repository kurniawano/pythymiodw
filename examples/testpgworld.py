from pythymiodw import ThymioSimPG
from pgworld import *

robot=ThymioSimPG(thymio_world)
robot.sleep(1)
print('move')
robot.wheels(200,200)
robot.sleep(15)

print('stop')
robot.wheels(0,0)
robot.quit()