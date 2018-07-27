import turtle
import pygame

class Point:
    def __init__(self, x=0,y=0):
        self.x=x
        self.y=y

class Block:
    def __init__(self, ll,ur):
        self.ll=ll
        self.ur=ur

    def is_overlap(self,p):
        if self.ll.x <= p.x <= self.ur.x and \
          self.ll.y <= p.y <= self.ur.y:
            return True
        else:
            return False

class Floor(Block):
    def __init__(self, ll, ur, color=(255,255,255)):
        Block.__init__(self,ll, ur)
        self._color = color


    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    color = property(get_color, set_color)


class Wall(Block):
    def __init__(self, ll, ur, height=10):
        Block.__init__(self,ll,ur)
        self._height = height

    def get_height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    height = property(get_height, set_height)

class World:
    def __init__(self, blocks,init_pos=None, init_heading=0):
        self.blocks=blocks
        self.init_heading=init_heading
        if init_pos !=None:
            self.init_pos=init_pos
        else:
            ll,ur=self.get_world_boundaries()
            self.init_pos=Point(abs(ur.x-ll.x)//2,abs(ur.y-ll.y)//2)
        
    def get_init_pos(self):
        return self.init_pos

    def get_init_heading(self):
        return self.init_heading

    def is_overlap(self,p):
        for b in self.blocks:
            if b.is_overlap(p):
                return True
        return False

    def get_centre_world(self):
        ll,ur=self.get_world_boundaries()
        xc=abs(ur.x-ll.x)//2
        yc=abs(ur.y-ll.y)//2
        return Point(xc,yc)

    def get_world_boundaries(self):
        min_x=self.blocks[0].ll.x
        min_y=self.blocks[0].ll.y
        max_x=self.blocks[0].ll.x
        max_y=self.blocks[0].ll.y
        for b in self.blocks:
            ll_x=b.ll.x
            ll_y=b.ll.y
            ur_x=b.ur.x
            ur_y=b.ur.y
            min_x=min(min_x,ll_x,ur_x)
            min_y=min(min_y,ll_y,ur_y)
            max_x=max(max_x,ll_x,ur_x)
            max_y=max(max_y,ll_y,ur_y)
        ll=Point(min_x,min_y)
        ur=Point(max_x,max_y)
        return ll,ur 

    def draw_world(self,t):
        for b in self.blocks:
            self.draw_block(t,b)

    def draw_block(self,t,b):
        t.penup()
        t.setposition(b.ll.x,b.ll.y)
        t.pendown()
        t.setx(b.ur.x)
        t.sety(b.ur.y)
        t.setx(b.ll.x)
        t.sety(b.ll.y)
        t.penup()

class PGWorld(World):
    def draw_block(self, robot, block):
        assert(block.ll.x<=block.ur.x and block.ll.y<=block.ur.y)
        if isinstance(block, Floor):
            pygame.draw.rect(robot.screen, block.color, (block.ll.x, block.ll.y, block.x_len, block.y_len))
        else:
            ul_x = block.ll.x
            ul_y = block.ll.y
            length = abs(float(block.ur.x) - float(block.ll.x))
            width = abs(float(block.ur.y)- float(block.ll.y))
            robot.screen.fill([0, 0, 0],rect=[ul_x,ul_y,length,width])