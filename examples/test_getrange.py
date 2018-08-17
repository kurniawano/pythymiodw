from pythymiodw import ThymioSimPG
from pgworld import thymio_world

robot = ThymioSimPG(thymio_world)
while True:
    print('position:', robot.robot._position)
    rect = robot.robot._image.get_rect()
    print('Rect (topleft):{}, (size):{}'.format(rect.topleft, rect.size))
    print('horizontal range sensor:', robot.robot.get_range_points_of_sensor())
    robot.sleep(1)

robot.quit()
