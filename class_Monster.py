import pygame

from lib import *
from class_MySprite import *

class Monster(MySprite):
    def __init__(self, pos, settings, g):
        MySprite.__init__(self, pos, [-1, 0], settings, g)
        
        self.width = 43
        self.height = 28
        
        self.image_still, image_rect = load_image('enemies/slime_normal.png')
        self.image_dead, image_rect = load_image('enemies/slime_dead.png')
        self.image_walking, image_rect = load_image('enemies/slime_walk.png')
        
        self.image = None
    
    def get_tile_ahead(self):
        tile_ahead = list(self.get_bottom_tile())
        if self._vel[0] < 0:
            tile_ahead[0] -= 1
        elif self._vel[0] > 0:
            tile_ahead[0] += 1
        return tile_ahead
    
    def update(self, dt):
        self._pos[0] += self._vel[0]
        #self._pos[1] += self._vel[1]
        
        draw_pos = (self._pos[0] - self.g.camera_x, self._pos[1])
        self.rect = pygame.Rect(draw_pos, (self.width, self.height))
        
        # have they bumped into anything
        tile_ahead = self.get_tile_ahead()
        if not self.g.world.is_tile_clear(tile_ahead):
            self._vel[0] *= -1
        else:
            # have they reached the end of a platform
            tile_ahead_and_below = self.get_tile_ahead()
            tile_ahead_and_below[1] += 1
            
            if self.g.world.is_tile_clear(tile_ahead_and_below):
                self._vel[0] *= -1
        
        if self._vel[0] != 0:
            self.image = self.image_walking
        else:
            self.image = self.image_still
    
    def die(self):
        print 'monster died'
