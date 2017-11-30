from pythymiodw.world import *

b1=Block(Point(0,0),Point(100,10))
b2=Block(Point(290,0),Point(300,100))
b3=Block(Point(200,290),Point(300,300))
b4=Block(Point(0,200),Point(10,300))
myworld=World([b1,b2,b3,b4],Point(50,250),init_heading=-90)

