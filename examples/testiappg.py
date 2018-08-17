from pythymiodw import *
from worldiapfinal import *

robot = ThymioSimPG(thymio_world, scale=3)  # create object
finish = False  # infinite loop
count = 0
while not finish:
    robot.wheels(300, 300)  # move forward
    robot.sleep(0.1)
    prox = robot.prox_horizontal  # check sensor
    print(prox[2])
    print(robot.robot.position())
    if prox[2] > 0:  # if there is obstacle turns
        count += 1
        if count >= 4:
            finish = True
        robot.wheels(0, 100)
        robot.sleep(3.7)
robot.quit()
