
class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Block:

    def __init__(self, ll, ur):
        self.ll = ll
        self.ur = ur

    def is_overlap(self, p, scale=1):
        if self.ll.x * scale <= p.x <= self.ur.x * scale and \
           self.ll.y * scale <= p.y <= self.ur.y * scale:
            return True
        else:
            return False

    def is_line_intersect(self, line, scale=1):
        x_len = abs(self.ur.x - self.ll.x)
        y_len = abs(self.ur.y - self.ll.y)
        corner1 = Point(self.ll.x, self.ll.y)
        corner2 = Point(corner1.x + x_len, corner1.y)
        corner3 = Point(corner1.x, corner1.y + y_len)
        corner4 = Point(self.ur.x, self.ur.y)
        ls = []
        lines = [Line(corner1, corner2), Line(corner1, corner3),
                 Line(corner2, corner4), Line(corner3, corner4)]
        for edge in lines:
            x = line.is_line_intersect(edge, scale)
            if x:
                ls.append(x)
        if ls == []:
            return False
        final = []
        for x, y in ls:
            final.append(((line.start.x * scale - x) ** 2 +
                          (line.start.y * scale - y) ** 2) ** 0.5)
        return ls[final.index(min(final))], min(final)


class Floor(Block):

    def __init__(self, ll, ur, color=(255, 255, 255)):
        Block.__init__(self, ll, ur)
        self._color = color

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    color = property(get_color, set_color)


class Wall(Block):

    def __init__(self, ll, ur, height=10):
        Block.__init__(self, ll, ur)
        self._height = height

    def get_height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    height = property(get_height, set_height)


class World:

    def __init__(self, blocks, init_pos=None, init_heading=0):
        self.blocks = blocks
        self.init_heading = init_heading
        if init_pos is not None:
            self.init_pos = init_pos
        else:
            ll, ur = self.get_world_boundaries()
            self.init_pos = Point(abs(ur.x - ll.x) // 2, abs(ur.y - ll.y) // 2)

    def get_init_pos(self):
        return self.init_pos

    def get_init_heading(self):
        return self.init_heading

    def is_overlap(self, p, scale=1):
        for b in self.blocks:
            if b.is_overlap(p, scale):
                return True
        return False

    def get_centre_world(self):
        ll, ur = self.get_world_boundaries()
        xc = abs(ur.x - ll.x) // 2
        yc = abs(ur.y - ll.y) // 2
        return Point(xc, yc)

    def get_world_boundaries(self):
        min_x = self.blocks[0].ll.x
        min_y = self.blocks[0].ll.y
        max_x = self.blocks[0].ll.x
        max_y = self.blocks[0].ll.y
        for b in self.blocks:
            ll_x = b.ll.x
            ll_y = b.ll.y
            ur_x = b.ur.x
            ur_y = b.ur.y
            min_x = min(min_x, ll_x, ur_x)
            min_y = min(min_y, ll_y, ur_y)
            max_x = max(max_x, ll_x, ur_x)
            max_y = max(max_y, ll_y, ur_y)
        ll = Point(min_x, min_y)
        ur = Point(max_x, max_y)
        return ll, ur

    def draw_world(self, t, scale=1):
        for b in self.blocks:
            self.draw_block(t, b)

    def draw_block(self, t, b):
        t.penup()
        t.setposition(b.ll.x, b.ll.y)
        t.pendown()
        t.setx(b.ur.x)
        t.sety(b.ur.y)
        t.setx(b.ll.x)
        t.sety(b.ll.y)
        t.penup()


class PGWorld(World):

    def draw_world(self, robot, scale=1):
        for b in self.blocks:
            self.draw_block(robot, b, scale)

    def draw_block(self, robot, block, scale=1):
        assert(block.ll.x <= block.ur.x and block.ll.y <= block.ur.y)
        length = abs(float(block.ur.x) - float(block.ll.x)) * scale
        width = abs(float(block.ur.y) - float(block.ll.y)) * scale
        ul_x = block.ll.x * scale
        ul_y = (robot.window.size[1] - block.ll.y * scale - width)
        ll, ur = self.get_world_boundaries()

        if isinstance(block, Floor):
            robot.window.screen.fill(block.color,
                                     rect=[ul_x, ul_y, length, width])
        else:
            robot.window.screen.fill([0, 0, 0],
                                     rect=[ul_x, ul_y, length, width])


class Line:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        if self.end.x != self.start.x:
            self.grad = (self.end.y -
                         self.start.y) / (self.end.x - self.start.x)
            self.c = self.start.y - self.grad * self.start.x
        else:
            self.grad = None
            self.c = None

    def is_line_intersect(self, line, scale=1):
        eps = 1e-7
        if self.grad is not None and line.grad is None:
            y = (self.grad * line.start.x + self.c) * scale
            x = line.start.x * scale
            if (self.start.x * scale - eps <= x <= self.end.x * scale + eps or
                self.start.x * scale + eps >= x >= self.end.x * scale - eps) and \
                (line.start.y * scale - eps <= y <= line.end.y * scale + eps or
                 line.start.y * scale + eps >= y >= line.end.y * scale - eps):
                return (x, y)
            else:
                return False
        elif line.grad is not None and self.grad is None:
            y = (line.grad * self.start.x + line.c)* scale
            x = self.start.x * scale
            if (line.start.x * scale - eps <= x <= line.end.x * scale + eps or
                line.start.x * scale + eps >= x >= line.end.x * scale- eps) and \
                (self.start.y * scale - eps <= y <= self.end.y * scale + eps or
                 self.start.y * scale + eps >= y >= self.end.y * scale - eps):
                return (x, y)
            else:
                return False
        if self.grad == line.grad:
            return False
        x = (self.c - line.c) / (line.grad - self.grad) 
        y = (self.grad * x + self.c)
        x *= scale
        y *= scale

        if (self.start.x * scale - eps <= x <= self.end.x * scale + eps or
            self.start.x * scale + eps >= x >= self.end.x * scale - eps) and \
            (self.start.y * scale - eps <= y <= self.end.y * scale + eps or
             self.start.y * scale + eps >= y >= self.end.y * scale - eps) and \
             (line.start.x * scale - eps <= x <= line.end.x * scale + eps or
              line.start.x * scale + eps >= x >= line.end.x * scale - eps) and \
              (line.start.y * scale - eps <= y <= line.end.y * scale + eps or
               line.start.y * scale + eps >= y >= line.end.y * scale - eps):
            return (x, y)
        return False
