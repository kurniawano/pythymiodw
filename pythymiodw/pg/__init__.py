import pygame
import math
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../images/"
abs_file_path = os.path.join(script_dir, rel_path)

background=[255,255,255] # white

class PGRobot(pygame.sprite.Sprite):
    def __init__(self,screen,filename='thymio.png',size=(32,32)):#size is (width,height). Measurement in pixels
        self.image = pygame.image.load(abs_file_path+filename)
        self._image = self.image
        self.screen = screen
        self._screenwidth,self._screenheight = self.screen.get_size()
        self._position=(self._screenwidth//2, self._screenheight//2)
        self._dimension = self._image.get_rect()
        #self._position = (self._screenwidth//2 - self._dimension.center[0], self._screenheight//2 - self._dimension.center[1])
    
    def setposition(self,x,y):#position is a Point object.
        self._position = (x,y)
        self.screen.blit(self.image,self._position)
        pygame.display.update()


    def rotate_and_centre(self,degrees):
        self._image = pygame.transform.rotate(self.image, degrees)
        self.rect = self._image.get_rect()
        #print("Rect size is {}".format(self.rect.size))
        #newpos = (self._position)
        newpos = (self._position[0]-self.rect.center[0],self._position[1]-self.rect.center[1])
        self.screen.blit(self._image,newpos)
        pygame.display.update()
        pygame.draw.rect(self.screen,[255,255,255],pygame.Rect((newpos),(80,80)))
        pygame.display.update()
        self.screen.blit(self._image,newpos)
        pygame.display.update()

        
    def setheading(self,heading):
        self._heading = heading
        self.rotate_and_centre(heading)
        
    
    def heading(self):
        return self._heading

    def forward(self,dist):
        D2R = (math.pi * 2)/360
        DIRECTION_VECTOR_LOOKUP = list([[math.cos(D2R*degrees),math.sin(D2R*degrees)] for degrees in range(360)])
        dx,dy = DIRECTION_VECTOR_LOOKUP[int(self._heading)]
        self.setposition(self._position[0]+dx,self._position[1]-dy)

    def position(self):
        return self._position
        
        

class PGScreen:
    def __init__(self,dimension=(800,600)):
        self.screen = pygame.display.set_mode(dimension)
        self.screen.fill(background)

    def setworldcoordinates(self,llx,lly,urx,ury):
        width = abs(urx-llx)
        height = abs(ury-lly)
        self.screen=pygame.display.set_mode((width,height))
        self.screen.fill(background)
        
