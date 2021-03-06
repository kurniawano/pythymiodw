import sys
import time
sys.path.append('..')

from pythymiodw.world import *
from pythymiodw import ThymioSim

tl=Point(10,10)
br=Point(20,20)
block=Block(tl,br)
print('lower left: ({:d},{:d})'.format(block.ll.x,block.ll.y))
print('upper right: ({:d},{:d})'.format(block.ur.x,block.ur.y))

p1=Point(15,15)
print('p1 in block? ',block.is_overlap(p1))
p2=Point(5,15)
print('p2 in block? ',block.is_overlap(p2))

b1=Block(Point(0,0),Point(100,10))
b2=Block(Point(0,0),Point(10,100))
b3=Block(Point(0,90),Point(100,100))
b4=Block(Point(90,0),Point(100,100))
world=World([b1,b2,b3,b4],Point(20,20),init_heading=270)
print('p1 in wall?', world.is_overlap(p1))
print('p2 in wall?', world.is_overlap(p2))
wll,wur=world.get_world_boundaries()
print('lower left of wall: ({:d},{:d})'.format(wll.x,wll.y))
print('upper right of wall: ({:d},{:d})'.format(wur.x,wur.y))
robot=ThymioSim(world)
time.sleep(2)
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
time.sleep(1)
