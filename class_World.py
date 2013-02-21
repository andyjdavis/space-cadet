import pygame

from lib import *
from class_Monster import *
from class_Goal import *

class World():
    def __init__(self, settings, g):
        self.monsters = pygame.sprite.RenderPlain()

        image, image_rect = load_image('maps/map2.png', None)
        
        self.map = [x[:] for x in [[0] * image_rect.width] * image_rect.height]

        for row in range(image_rect.height):
            for col in range(image_rect.width):
                pixel_color = image.get_at((col,row))
                if pixel_color[0] == 0 and pixel_color[1] == 0 and pixel_color[2] == 0:
                    # ground
                    self.map[row][col] = 1
                if pixel_color[0] == 0 and pixel_color[1] == 255 and pixel_color[2] == 0:
                    # monster
                    pos = [col * settings.block_width, row * settings.block_width]
                    monster = Monster(pos, settings, g)
                    self.monsters.add(monster)
                if pixel_color[0] == 255 and pixel_color[1] == 255 and pixel_color[2] == 0:
                    # goal
                    pos = [col * settings.block_width, row * settings.block_width]
                    self.goal = Goal(pos, settings, g)

        self.width = image_rect.width
        self.height = len(self.map)
        
        self.settings = settings
        self.g = g
        
        self.block_image, block_image_rect = load_image("ground.png", None)
        
        #blocks_image, blocks_image_rect = load_image("ground.png", None)
        #self.block_image = blocks_image.subsurface((240, 1), (270, 31))
        
        #self.block_image = pygame.Surface((settings.block_width,settings.block_width)).convert()
        #self.block_image.fill((240, 119, 70))
        
        self.empty_tile_image = pygame.Surface((settings.block_width,settings.block_width)).convert()
        # light sky blue
        self.empty_tile_image.fill((135, 206, 250))

    def animation_update(self):
        #for monster in self.monsters:
        #    monster.animation_update()
        self.g.player.animation_update()
    
    def update(self, dt):
        self.monsters.update(dt)
        self.goal.update(dt)
    
    def pos_to_tile(self, pos):
        x = pos[0]/self.settings.block_width
        y = pos[1]/self.settings.block_width
        return (x, y)
    
    # returns top left of the tile
    def tile_to_pos(self, tile):
        x = tile[0] * self.settings.block_width
        y = tile[1] * self.settings.block_width
        return (x, y)
    
    def get_tile(self, x, y):
        return self.map[y][x]
    
    def is_tile_clear(self, coords):
        if coords[0] >= self.width or coords[1] >= self.height:
            return False
        else:
            return self.get_tile(coords[0], coords[1]) == 0
    
    def is_sprite_colliding_with_scenery(self, sprite):
        tiles = sprite.get_tiles()
        for tile in tiles:
            if not self.is_tile_clear(tile):
                # need to do smarter collision detection here
                return True
        return False
    
    def clear_tile(self, tile):
        if not self.is_tile_clear(tile):
            # Do we need to do anything else here?
            self.map[tile[1]][tile[0]] = 0
    
    def clear_tiles(self, tiles):
        for tile in tiles:
            self.clear_tile(tile)
    
    def draw(self, screen):
        self.image = pygame.Surface(screen.get_size()).convert()
        
        for x in range(self.width):
            for y in range(self.height):
                if self.get_tile(x, y) != 0:
                    self.image.blit(
                        self.block_image,
                        (x * self.settings.block_width - self.g.camera_x, y * self.settings.block_width)
                    )
                else:
                    self.image.blit(
                        self.empty_tile_image,
                        (x * self.settings.block_width - self.g.camera_x, y * self.settings.block_width)
                    )
        
        screen.blit(self.image, (0,0))
        self.monsters.draw(screen)
        self.goal.draw(screen)
        
