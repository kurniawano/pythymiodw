from pythymiodw import ThymioSimPG
from pgworld import thymio_world

robot = ThymioSimPG(thymio_world)
while True:
	print('position:',robot.robot._position)
	rect = robot.robot._image.get_rect()
	print('Rect (topleft):{}, (size):{}'.format(rect.topleft, rect.size))
	print('center robot:',robot.robot.get_center_robot())
	robot.sleep(1)
	
robot.quit()