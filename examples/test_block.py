from pythymiodw.world import *

b1 = Block(Point(0, 0), Point(100, 10))
l1 = Line(Point(50, 50), Point(50, 0))
print(b1.is_line_intersect(l1, scale=1))
print(b1.is_line_intersect(l1, scale=3))
