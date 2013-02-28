import pygame

from lib import *
from class_MySprite import *

class Goal(MySprite):
    def __init__(self, pos, settings, g):
        MySprite.__init__(self, pos, (0, 0), settings, g)
        
        self.width = 39
        self.height = 34
        
        self.image, image_rect = load_image('shroom.png')
    
    def update(self, dt):
        draw_pos = (self._pos[0] - self.g.camera_x, self._pos[1] - self.g.camera_y)
        self.rect = pygame.Rect(draw_pos, (self.width, self.height))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
