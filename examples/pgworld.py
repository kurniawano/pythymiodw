from pythymiodw.world import *

b1=Block(Point(0,0),Point(100,0))
b2=Block(Point(200,0),Point(200,100))
b3=Block(Point(100,200),Point(200,200))
b4=Block(Point(0,100),Point(00,200))
thymio_world=PGWorld([b1,b2,b3,b4],Point(100,100),init_heading=-90)