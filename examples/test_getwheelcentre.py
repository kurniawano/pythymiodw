from pythymiodw import ThymioSimPG
from pgworld import thymio_world

robot = ThymioSimPG(thymio_world, scale=1)
while True:
	print('position:',robot.robot._position)
	rect = robot.robot._image.get_rect()
	print('Rect (topleft):{}, (size):{}'.format(rect.topleft, rect.size))
	print('center wheels:',robot.robot.get_center_wheels())
	robot.sleep(1)
	
robot.quit()