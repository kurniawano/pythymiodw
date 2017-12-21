from pythymiodw import *

robot=ThymioReal()
robot.init_read()

while True:
    ground=robot.prox_ground
    print(ground.delta[0],ground.delta[1])
    if 0<ground.delta[0]<500 or 0<ground.delta[1]<500:
        break
    robot.wheels(100,100)
robot.quit()
