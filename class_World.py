import pygame

from lib import *
from class_Monster import *
from class_Goal import *

class World():
    def __init__(self, settings, g):
        self.settings = settings
        self.g = g
        
        self.block_image, block_image_rect = load_image("ground.png", None)
        #self.bad_block_image, block_image_rect = load_image("spikes.png", None, True)
        
        self.empty_tile_image = pygame.Surface((settings.block_width,settings.block_width)).convert()
        # light sky blue
        self.empty_tile_image.fill(self.settings.background_color)
        
        self.monsters = pygame.sprite.RenderPlain()
        self.goals = pygame.sprite.RenderPlain()

        image, image_rect = load_image('maps/map' + str(self.g.level) + '.png', None)
        
        self.map = [x[:] for x in [[0] * image_rect.width] * image_rect.height]

        for row in range(image_rect.height):
            for col in range(image_rect.width):
                pixel_color = image.get_at((col,row))
                if pixel_color[0] == 0 and pixel_color[1] == 0 and pixel_color[2] == 0:
                    # black = ground
                    self.map[row][col] = 1
                if pixel_color[0] == 0 and pixel_color[1] == 255 and pixel_color[2] == 0:
                    # green = monster
                    pos = [col * settings.block_width, row * settings.block_width]
                    self.monsters.add(Monster(pos, settings, g))
                if pixel_color[0] == 255 and pixel_color[1] == 255 and pixel_color[2] == 0:
                    # yellow = goal
                    pos = [col * settings.block_width, row * settings.block_width]
                    self.goals.add(Goal(pos, settings, g))
        
        self.width = image_rect.width
        self.height = len(self.map)
        
        self.image = None
        
        #check that all bottom row tiles are either terrain or lava/spikes or whatever
        #for tile_x in range(len(self.map)):
        #    print tile_x
        #    if self.is_tile_clear((tile_x, self.height - 1)):
        #        print 'found empty'
        #        self.map[self.height - 1][tile_x] = 2

    def animation_update(self):
        #for monster in self.monsters:
        #    monster.animation_update()
        self.g.player.animation_update()
    
    def update(self, dt):
        self.monsters.update(dt)
        self.goals.update(dt)
    
    def pos_to_tile(self, pos):
        x = int(pos[0]/self.settings.block_width)
        y = int(pos[1]/self.settings.block_width)

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
        if not self.image:
            self.image = pygame.Surface(screen.get_size()).convert()
        
        x_start_tile = self.pos_to_tile((self.g.camera_x, self.g.camera_y))
        x_end_tile = self.pos_to_tile((self.g.camera_x + self.settings.width, self.g.camera_y))
        
        y_start_tile = self.pos_to_tile((self.g.camera_x, self.g.camera_y))
        y_end_tile = self.pos_to_tile((self.g.camera_x, self.g.camera_y + self.settings.height))
        
        for x in range(x_start_tile[0], x_end_tile[0]):
            for y in range(y_start_tile[1], y_end_tile[1]):
                tile = self.get_tile(x, y)
                if tile == 1:
                    self.image.blit(
                        self.block_image,
                        (x * self.settings.block_width - self.g.camera_x, y * self.settings.block_width - self.g.camera_y)
                    )
                elif tile == 2:
                    self.image.blit(
                        self.bad_block_image,
                        (x * self.settings.block_width - self.g.camera_x, y * self.settings.block_width - self.g.camera_y)
                    )
                else:
                    self.image.blit(
                        self.empty_tile_image,
                        (x * self.settings.block_width - self.g.camera_x, y * self.settings.block_width - self.g.camera_y)
                    )
        
        screen.blit(self.image, (0,0))
        self.monsters.draw(screen)
        self.goals.draw(screen)
        
