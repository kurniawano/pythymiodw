from pythymiodw import ThymioSimPG

robot=ThymioSimPG(scale = 3)
robot.sleep(1)
print('move')
robot.wheels(100,100)
robot.sleep(5)
robot.wheels(0,100)
robot.sleep(4)
robot.wheels(100,100)
robot.sleep(5)
robot.wheels(100,0)
robot.sleep(4)
robot.wheels(100,100)
robot.sleep(5)
print('stop')
robot.wheels(0,0)
robot.quit()
