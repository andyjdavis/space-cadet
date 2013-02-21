import os, pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

import math
import random

from class_World import World
from class_Player import Player

class Settings:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.resourcepath = 'resources'
        self.block_width = 30
        self.player_move_acc = 700
        self.player_jump = 1200
        self.gravity = 2200
        self.friction = 0.8
settings = Settings()

class Globals:
    def __init__(self):
        self.world = None
        self.player = None
        self.camera_x = 0
g = Globals()

pygame.init()
screen = pygame.display.set_mode((settings.width, settings.height))
pygame.display.set_caption('My Game')
#pygame.mouse.set_visible(0)

sprite_group = pygame.sprite.RenderPlain()

def load_world():
    g.world = World(settings, g)
    g.player = Player([settings.block_width,settings.block_width], settings, g)
    g.camera_x = 0

def key_down(k):
    if k == K_LEFT:
        g.player.walk_left()
    elif k == K_RIGHT:
        g.player.walk_right()
    elif k == K_SPACE:
        g.player.jump()

def key_up(k):
    pass
    if k == K_LEFT:
        g.player.walk_left_stop()
    elif k == K_RIGHT:
        g.player.walk_right_stop()

def main():
    
    load_world()
    
    bg = pygame.Surface(screen.get_size()).convert()
    bg.fill((255, 255, 255))
    #bg.blit(nebula_image, screen.get_rect(), nebula_image.get_rect())
        
    clock = pygame.time.Clock()
    
    # 30 per second
    pygame.time.set_timer(USEREVENT + 1, 33)
    
    dt = 0
    reset_level = False

    while 1:
        
        dt = clock.tick()/1000.00
        
        g.world.update(dt)
        g.player.update(dt)
        
        reset_level = False
        
        # Did the player touch a monster?
        monsters_hit = pygame.sprite.spritecollide(g.player, g.world.monsters, False)
        for monster in monsters_hit:
            reset_level = True
        
        # Did the player reach the goal?
        if g.player.rect.colliderect(g.world.goal.rect):
            print 'success'
                
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                else:
                    key_down(event.key)
            elif event.type == KEYUP:
                key_up(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                pass
            elif event.type == USEREVENT + 1:
                g.world.animation_update()

        if reset_level:
            load_world()
        else:        
            screen.blit(bg, (0, 0))
            g.world.draw(screen)
            g.player.draw(screen)
        
            pygame.display.flip()
            
            if g.player.rect[0] > settings.width/2:
                g.camera_x += 2
            elif g.player.rect[0] < settings.width/4:
                g.camera_x -= 2
                if g.camera_x < 0:
                    g.camera_x = 0

if __name__ == '__main__': main()

