import pygame
import math
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "images/"
abs_file_path = os.path.join(script_dir, rel_path)

class PGRobot(pygame.sprite.Sprite):
    def __init__(self,window, scale = 1):#size is (width,height). Measurement in pixels
        filename = {1:'thymio1.png', 2:'thymio2.png', 3:'thymio3.png',
                    4:'thymio4.png', 5:'thymio5.png'}
        self._scale = scale
        self.__image = pygame.image.load(abs_file_path+filename[scale]).convert_alpha()
        self._image = self.__image
        self.window = window
        self._screenwidth,self._screenheight = self.window.screen.get_size()
        self._position=(self._screenwidth//2, self._screenheight//2)
        self._dimension = self._image.get_rect()
    
    def setposition(self,x,y):#position is a Point object.
        self._position = (x,y) # top left corner
        rect = self._image.get_rect()
        width = self.window.size[1]
        y= width - y
        newpos = (x - rect.center[0], y - rect.center[1]) # centralized position
        self.window.screen.blit(self._image, newpos)
        pygame.display.update()


    def rotate_and_centre(self,degrees):
        self._image = pygame.transform.rotate(self.__image, degrees)
        rect = self._image.get_rect()
        newpos = (self._position[0] - rect.center[0],self._position[1] - rect.center[1])
        self.window.screen.blit(self._image, newpos)
        
    def setheading(self,heading):
        self._heading = heading
        self.rotate_and_centre(heading)
        
    
    def heading(self):
        return self._heading

    def forward(self,dist):
        D2R = (math.pi * 2) / 360
        DIRECTION_VECTOR_LOOKUP = list([[dist * math.cos(D2R * degrees), dist * math.sin(D2R * degrees)] for degrees in range(360)])
        self._heading = self._heading % 360
        dx, dy = DIRECTION_VECTOR_LOOKUP[int(self._heading)]
        dx *= self._scale
        dy *= self._scale
        self.setposition(self._position[0] + dx, self._position[-1] + dy)

    def position(self):
        return self._position
        
    def get_ground_sensor_position(self):
        x_pos, y_pos = self.get_center_wheels()
        rect = self._image.get_rect()
        x_pos =  x_pos + 7*math.cos(self._heading*math.pi/180)*self._scale
        y_pos =  y_pos -7*math.sin(self._heading*math.pi/180)*self._scale
                   
        x_pos1 = x_pos - math.sin(self._heading*math.pi/180)*self._scale
        y_pos1 = y_pos - math.cos(self._heading*math.pi/180)*self._scale
        x_pos2 = x_pos + math.sin(self._heading*math.pi/180)*self._scale
        y_pos2 = y_pos + math.cos(self._heading*math.pi/180)*self._scale
        return ((x_pos1, y_pos1), (x_pos2, y_pos2))

    def get_center_wheels(self):
        head = self._heading%360
        #robot = pygame.transform.rotate(self._image, -head)
        x = self._image.get_rect()
        print(self._position)
        x_cpos = self._position[0] - 3*math.cos(head*math.pi/180)*self._scale
        y_cpos = self._position[1] - 3*math.sin(head*math.pi/180)*self._scale
        return x_cpos, y_cpos

    def get_center_robot(self):
        x_pos, y_pos = self.get_center_wheels()
        x_pos =  x_pos + 3*math.cos(self._heading*math.pi/180)*self._scale
        y_pos =  y_pos - 3*math.sin(self._heading*math.pi/180)*self._scale
        return x_pos, y_pos

    def get_horizontal_sensor_position(self):
        x, y = self.get_center_wheels()
        distance = 8
        #centre sensor
        x2 = x + distance*math.cos(self._heading*math.pi/180)*self._scale
        y2 = y - distance*math.sin(self._heading*math.pi/180)*self._scale
        x3 = x + distance*math.cos(self._heading*math.pi/180-math.pi/8)*self._scale
        y3 = y - distance*math.sin(self._heading*math.pi/180-math.pi/8)*self._scale
        x4 = x + distance*math.cos(self._heading*math.pi/180-math.pi/4)*self._scale
        y4 = y - distance*math.sin(self._heading*math.pi/180-math.pi/4)*self._scale
        x1 = x + distance*math.cos(self._heading*math.pi/180+math.pi/8)*self._scale
        y1 = y - distance*math.sin(self._heading*math.pi/180+math.pi/8)*self._scale
        x0 = x + distance*math.cos(self._heading*math.pi/180+math.pi/4)*self._scale
        y0 = y - distance*math.sin(self._heading*math.pi/180+math.pi/4)*self._scale
        x_pos, y_pos = self.get_center_wheels()
        x6 = x_pos + 3*math.sin(self._heading*math.pi/180)*self._scale
        y6 = y_pos + 3*math.cos(self._heading*math.pi/180)*self._scale
        x5 = x_pos - 3*math.sin(self._heading*math.pi/180)*self._scale
        y5 = y_pos - 3*math.cos(self._heading*math.pi/180)*self._scale
        return ((x0,y0),(x1,y1),(x2,y2),(x3,y3),(x4,y4), (x5,y5), (x6, y6))

    def get_range_points_of_sensor(self):
        distance = 11
        x, y = self.get_center_wheels()
        x2 = x + distance*math.cos(self._heading*math.pi/180)*self._scale
        y2 = y - distance*math.sin(self._heading*math.pi/180)*self._scale
        x3 = x + distance*math.cos(self._heading*math.pi/180-math.pi/8)*self._scale
        y3 = y - distance*math.sin(self._heading*math.pi/180-math.pi/8)*self._scale
        x4 = x + distance*math.cos(self._heading*math.pi/180-math.pi/4)*self._scale
        y4 = y - distance*math.sin(self._heading*math.pi/180-math.pi/4)*self._scale
        x1 = x + distance*math.cos(self._heading*math.pi/180+math.pi/8)*self._scale
        y1 = y - distance*math.sin(self._heading*math.pi/180+math.pi/8)*self._scale
        x0 = x + distance*math.cos(self._heading*math.pi/180+math.pi/4)*self._scale
        y0 = y - distance*math.sin(self._heading*math.pi/180+math.pi/4)*self._scale
        distance = 9
        x_pos, y_pos = self.get_center_wheels()
        x6 = x_pos + 3*math.sin(self._heading*math.pi/180)*self._scale - distance*math.cos(self._heading*math.pi/180)*self._scale
        y6 = y_pos + 3*math.cos(self._heading*math.pi/180)*self._scale + distance*math.sin(self._heading*math.pi/180)*self._scale
        x5 = x_pos - 3*math.sin(self._heading*math.pi/180)*self._scale - distance*math.cos(self._heading*math.pi/180)*self._scale
        y5 = y_pos - 3*math.cos(self._heading*math.pi/180)*self._scale + distance*math.sin(self._heading*math.pi/180)*self._scale
        return ((x0,y0),(x1,y1),(x2,y2),(x3,y3),(x4,y4), (x5, y5), (x6, y6))

class PGWindow:
    def __init__(self,size=(100,100), color=(255,255,255), scale = 1):
        size = size[0]*scale, size[1]*scale
        self.scale = scale
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.color = color
        self.screen.fill(self.color)

    def setworldcoordinates(self,llx,lly,urx,ury):
        width = abs(urx-llx)*self.scale
        height = abs(ury-lly)*self.scale
        self.screen=pygame.display.set_mode((width,height))
        self.size = (width, height)
        self.screen.fill(self.color)
        
