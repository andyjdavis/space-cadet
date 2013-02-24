import pygame

from lib import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self, pos, settings, g):
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = pos
        self.settings = settings
        self.g = g
        
        self.images = []
        self.current_image_index = 0
    
    def update(self):
        pass
    
    def animation_update(self):
        if len(self.images) > 0:
            self.current_image_index += 1
            self.current_image_index %= len(self.images)
        else:
            self.current_image_index = 0
    
    def get_tiles(self):
        top_left = self.g.world.pos_to_tile(self.pos)
        bottom_right = self.g.world.pos_to_tile((self.pos[0]+self.width, self.pos[1]+self.height))
        
        tiles = []
        
        y = top_left[1]
        while y <= bottom_right[1]:
            x = top_left[0]
            while x <= bottom_right[0]:
                tiles.append((x,y))
                x += 1
            y += 1
        
        return tiles
    
    def get_bottom_tile(self):
        tiles = self.get_tiles()
        bottom = None
        for tile in tiles:
            if bottom == None or bottom[1] < tile[1]:
                bottom = tile
        return bottom
