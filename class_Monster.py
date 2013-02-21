import pygame

from lib import *
from class_MySprite import *

class Monster(MySprite):
    def __init__(self, pos, settings, g):
        MySprite.__init__(self, pos, settings, g)
        
        self.width = 43
        self.height = 28
        
        self.vel = [-1, 0]
        
        self.image_still, image_rect = load_image('enemies/slime_normal.png')
        self.image_dead, image_rect = load_image('enemies/slime_dead.png')
        self.image_walking, image_rect = load_image('enemies/slime_walk.png')
        
        self.image = None
    
    def update(self, dt):
        self.pos[0] += self.vel[0]
        #self.pos[1] += self.vel[1]
        
        draw_pos = (self.pos[0] - self.g.camera_x, self.pos[1])
        self.rect = pygame.Rect(draw_pos, (self.width, self.height))
        
        # have they reached the end of a platform
        bottom = self.get_bottom_tile()
        tile_ahead = list(bottom)
        tile_ahead[1] += 1
        if self.vel[0] < 0:
            tile_ahead[0] -= 1
        elif self.vel[0] > 0:
            tile_ahead[0] += 1
        
        if self.g.world.is_tile_clear(tile_ahead):
            self.vel[0] *= -1
        
        if self.vel[0] != 0:
            self.image = self.image_walking
        else:
            self.image = self.image_still
    
    def die(self):
        print 'monster died'
