import pygame

from lib import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self, pos, vel, settings, g):
        pygame.sprite.Sprite.__init__(self)
        
        self._pos = pos
        self._vel = vel
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
    
    def get_pos(self):
        return self._pos
    
    def get_tiles(self):
        pos = self.get_pos()
        top_left_tile = self.g.world.pos_to_tile(pos)
        bottom_right_tile = self.g.world.pos_to_tile( (pos[0]+self.width, pos[1]+self.height) )
        
        tiles = []
        
        y = top_left_tile[1]
        while y <= bottom_right_tile[1]:
            x = top_left_tile[0]
            while x <= bottom_right_tile[0]:
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
    
    def get_tile_ahead(self, pixels_ahead = 1):
        future_x = None
        if self._vel[0] < 0:
            future_x = self._pos[0] - pixels_ahead
        if self._vel[0] > 0:
            future_x = self._pos[0] + self.width + pixels_ahead
        return self.g.world.pos_to_tile((future_x, self._pos[1] + self.height))
    
    def get_tile_ahead_and_below(self, pixels_ahead = 1):
        tile = self.get_tile_ahead(pixels_ahead)
        return (tile[0], tile[1] + 1)

