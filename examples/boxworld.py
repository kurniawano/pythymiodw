from pythymiodw.world import *

b1 = Wall(Point(0, 0), Point(200, 10))
b2 = Wall(Point(190, 0), Point(200, 200))
b3 = Wall(Point(0, 190), Point(200, 200))
b4 = Wall(Point(0, 0), Point(10, 200))
thymio_world = World([b1, b2, b3, b4], Point(100, 100), init_heading=270)
