from pythymiodw import ThymioSimPG
from groundworld import thymio_world

robot = ThymioSimPG(thymio_world, scale = 3)
robot.wheels(100,100)
robot.sleep(2)
delta = robot.prox_ground.delta
delta = sum(delta)/2.0
print(delta)
while delta > 500:
	print(delta)
	robot.sleep(2)
	delta = robot.prox_ground.delta
	delta = sum(delta)/2.0
print(delta)
robot.quit()