import pygame
import math

from lib import *
from class_SmartSprite import *

class Player(SmartSprite):
    def __init__(self, pos, settings, g):
        SmartSprite.__init__(self, pos, [0, 0], settings, g)
        
        self.width = 75
        self.height = 96
        
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
        pos = self.get_pos()
        
        # check left side
        tile_below_player = self.g.world.pos_to_tile((pos[0], pos[1] + self.height + 1))
        if self.g.world.is_tile_clear(tile_below_player):
            # now check right
            tile_below_player = self.g.world.pos_to_tile((pos[0] + self.width, pos[1] + self.height + 1))
            if self.g.world.is_tile_clear(tile_below_player):
                return True
        return False

    def update(self, dt):
    
        self._future_pos = list(self._pos)
        
        if not (self.right_down and self.left_down):
            sign = 1
            if self.left_down:
                sign = -1
            
            if (self.right_down or self.left_down):
                self._vel[0] = self.settings.player_move_acc * sign
        
        # apply friction
        if not (self.right_down or self.left_down):
            if abs(self._vel[0]) < 1:
                self._vel[0] = 0
            else:
                self._vel[0] *= self.settings.friction
        
        # If they're in the air, apply gravity
        if self.in_the_air():
            gravity_vel_delta = (self.settings.gravity * dt)
            self._vel[1] += gravity_vel_delta
        
        deltax = self._vel[0] * dt * 0.5
        deltay = self._vel[1] * dt * 0.5
        
        future_x = calc_new_pos(self._future_pos[0], deltax)
        future_y = calc_new_pos(self._future_pos[1], deltay)
        
        x_collide = y_collide = False
        
        self._future_pos[0] = future_x
        if self.g.world.is_sprite_colliding_with_scenery(self):
            # stick with the old value
            x_collide = True
        
        # reset the x value so the y value can be tested independently
        self._future_pos[0] = self._pos[0]
        
        self._future_pos[1] = future_y
        if self.g.world.is_sprite_colliding_with_scenery(self):
            y_collide = True
            self._vel[1] = 0

        # test x and y together
        #self._future_pos[0] = future_x
        
        if x_collide:
            self._future_pos[0] = self._pos[0]
        else:
            self._future_pos[0] = future_x
        
        if y_collide:
            self._future_pos[1] = self._pos[1]
        else:
            self._future_pos[1] = future_y
        
        self.confirm_future()
        
        pos = self.get_pos()
        draw_pos = (pos[0] - self.g.camera_x, pos[1] - self.g.camera_y)
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
            self._vel[1] = -self.settings.player_jump;

