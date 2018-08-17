from pythymiodw.world import *

wall1 = Wall(Point(0,0), Point(100,10))
wall2 = Wall(Point(90,0), Point(100,100))
floor1 = Floor(Point(50,10), Point(90,100), color=[100,100,100])
thymio_world = PGWorld([wall1, wall2, floor1], init_pos=Point(30,30), init_heading = 0)