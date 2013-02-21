import pygame
import math

from lib import *
from class_MySprite import *

class Player(MySprite):
    def __init__(self, pos, settings, g):
        MySprite.__init__(self, pos, settings, g)
        
        self.width = 75
        self.height = 96
        
        self.vel = [0,0]
        
        # did we revert the last move?
        self.reverted = False
        
        self.left_down = False
        self.right_down = False
        
        self.current_image_index = 0
        for i in range(1, 12):
            formatted_i = str(i)
            if i < 10:
                formatted_i = '0' + str(i)
            image, image_rect = load_image('character/walk/walk00' + formatted_i + '.png')
            self.images.append(image)
    
    def in_the_air(self):
        # check left side
        tile_below_player = self.g.world.pos_to_tile((self.pos[0], self.pos[1] + self.height + 1))
        if self.g.world.is_tile_clear(tile_below_player):
            # now check right
            tile_below_player = self.g.world.pos_to_tile((self.pos[0] + self.width, self.pos[1] + self.height + 1))
            if self.g.world.is_tile_clear(tile_below_player):
                return True
        return False
            
    
    def update(self, dt):
        
        if not self.reverted:
            self.vel_previous = list(self.vel)
            self.pos_previous = list(self.pos)
        
        if not (self.right_down and self.left_down):
            sign = 1
            if self.left_down:
                sign = -1
            
            if (self.right_down or self.left_down):
                self.vel[0] = self.settings.player_move_acc * sign
        
        # apply friction
        if not (self.right_down or self.left_down):
            if abs(self.vel[0]) < 1:
                self.vel[0] = 0
            else:
                self.vel[0] *= self.settings.friction
        
        # If they're in the air, apply gravity
        gravity_vel_delta = (self.settings.gravity * dt)
        if self.in_the_air():
            self.vel[1] += gravity_vel_delta
        
        deltax = self.vel[0] * dt * 0.5
        deltay = self.vel[1] * dt * 0.5
        
        self.pos[0] = update_pos(self.pos[0], deltax)
        self.pos[1] = update_pos(self.pos[1], deltay)
        
        self.reverted = False
        
        if self.g.world.is_sprite_colliding_with_scenery(self):
            self.revert(True)
        
        draw_pos = (self.pos[0] - self.g.camera_x, self.pos[1])
        self.rect = pygame.Rect(draw_pos, (self.width, self.height))
        
        if self.left_down or self.right_down:
            self.image = self.images[self.current_image_index]
        else:
            self.current_image_index = 0
            self.image = self.images[self.current_image_index]
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def walk_right(self):
        self.right_down = True
    
    def walk_right_stop(self):
        self.right_down = False
    
    def walk_left(self):
        self.left_down = True
    
    def walk_left_stop(self):
        self.left_down = False
    
    def jump(self):
        if not self.in_the_air():
            self.vel[1] = -self.settings.player_jump;

