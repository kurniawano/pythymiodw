import pygame
import math
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "images/"
abs_file_path = os.path.join(script_dir, rel_path)


class PGRobot(pygame.sprite.Sprite):
    def __init__(self,window, filename='thymio.png',size=(32,32)):#size is (width,height). Measurement in pixels
        self.__image = pygame.image.load(abs_file_path+filename).convert_alpha()
        self._image = self.__image
        self.window = window
        self._screenwidth,self._screenheight = self.window.screen.get_size()
        self._position=(self._screenwidth//2, self._screenheight//2)
        self._dimension = self._image.get_rect()
    
    def setposition(self,x,y):#position is a Point object.
        self._position = (x,y) # top left corner
        rect = self._image.get_rect()
        newpos = (self._position[0] - rect.center[0], self._position[1] - rect.center[1]) # centralized position
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
        self.setposition(self._position[0] + dx, self._position[-1] - dy)

    def position(self):
        return self._position
        
        

class PGWindow:
    def __init__(self,size=(800,600), color=(255,255,255)):
        self.screen = pygame.display.set_mode(size)
        self.color = color
        self.screen.fill(self.color)
        self.size = size


    def setworldcoordinates(self,llx,lly,urx,ury):
        width = abs(urx-llx)
        height = abs(ury-lly)
        self.screen=pygame.display.set_mode((width,height))
        self.size = (width, height)
        self.screen.fill(self.color)
        
