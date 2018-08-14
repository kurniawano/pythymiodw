from pythymiodw.world import *

b1=Block(Point(0,0),Point(100,10))
b2=Block(Point(190,0),Point(200,100))
b3=Block(Point(100,190),Point(200,200))
b4=Block(Point(0,100),Point(10,200))
thymio_world=PGWorld([b1,b2,b3,b4],Point(50,50),init_heading=-90)