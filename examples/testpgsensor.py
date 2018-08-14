from pythymiodw import ThymioSimPG
from boxworld import *

robot = ThymioSimPG(thymio_world, scale=3)
robot.sleep(1)
print('move')
robot.wheels(200, 200)
while robot.prox_horizontal[2] == 0:
    print(robot.prox_horizontal[2])
    robot.sleep(1)

print('stop')
robot.wheels(0, 0)
robot.quit()
