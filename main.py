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
        self.width = 900 # 30 tiles wide
        self.height = 600 # 20 tiles high
        self.resourcepath = 'resources'
        self.block_width = 30
        self.player_move_acc = 700
        self.player_jump = 1200
        self.gravity = 2200
        self.friction = 0.8
        self.camera_speed = 10
        self.background_color = (135, 206, 250)
        
        self.splash_size = (600, 400)
        self.text_antialias = 1
        self.text_color = (0, 0, 0)
        #self.text_bg_color = (0, 0, 0)
settings = Settings()

class Globals:
    def __init__(self):
        self.level = 1
        self.world = None
        self.player = None
        self.camera_x = 0
        self.camera_y = 0
        
        self.state_playing = True
        self.state_end_game = False
        
        self.splash_surface = None
        
        self.mushroom_time = 1
g = Globals()

pygame.init()
screen = pygame.display.set_mode((settings.width, settings.height))
pygame.display.set_caption('My Game')
#pygame.mouse.set_visible(0)

sprite_group = pygame.sprite.RenderPlain()
g.score_font = pygame.font.SysFont("arial", 18)

def load_world():
    g.mushroom_time = 1
    g.camera_x = 0
    g.camera_y = 0
    
    if g.level > 10:
        # all levels complete
        g.state_playing = False
        g.state_end_game = True
    else:
        g.state_playing = True
        g.state_end_game = False
        
        g.world = World(settings, g)
        g.player = Player([settings.block_width,settings.block_width], settings, g)
        g.camera_x = 0

def key_down(k):
    if k == K_LEFT:
        g.player.walk_left()
    elif k == K_RIGHT:
        g.player.walk_right()
    elif k == K_SPACE:
        if g.state_playing:
            g.player.jump()
        elif g.state_end_game:
            g.level = 1
            load_world()

def key_up(k):
    pass
    if k == K_LEFT:
        g.player.walk_left_stop()
    elif k == K_RIGHT:
        g.player.walk_right_stop()

def display_end_game_splash(screen):
    if not g.splash_surface:
        g.splash_surface = pygame.Surface(settings.splash_size).convert()

        font_big = pygame.font.SysFont("arial",24)
        font_small = pygame.font.SysFont("arial", 18)
        
        text = font_big.render("You now have all the mushrooms in the world!!", settings.text_antialias, settings.text_color, settings.text_bg_color)
        g.splash_surface.blit(text, (10, 20))
        
        text = font_small.render("What you do with them is up to you...", settings.text_antialias, settings.text_color, settings.text_bg_color)
        g.splash_surface.blit(text, (10, 80))
        
        text = font_small.render("Press space to start over", settings.text_antialias, settings.text_color, settings.text_bg_color)
        g.splash_surface.blit(text, (10, 150))
    
    splash_dest_rect = pygame.Rect((settings.width/2) - (settings.splash_size[0]/2), (settings.height/2) - (settings.splash_size[1]/2), settings.splash_size[0], settings.splash_size[1])
    screen.blit(g.splash_surface, splash_dest_rect)

def draw_score(screen):
    message = str(len(g.world.goals)) + " mushrooms left"
    text = g.score_font.render(message, settings.text_antialias, settings.text_color, settings.background_color)
    screen.blit(text, (settings.width - 200, 80))

def draw_fps(screen, dt):
    pass
    #if dt > 0:
    #    message = str(1/dt) + " FPS"
    #    text = g.score_font.render(message, settings.text_antialias, settings.text_color, settings.background_color)
    #    screen.blit(text, (settings.width - 200, 160))

def update_camera_offsets():
    multiplier = g.player.rect[0]/float(settings.width)
    if g.player.rect[0] > settings.width * (1/3):
        delta = multiplier * settings.camera_speed
        if delta >= 1:
            g.camera_x += delta
            end_world = g.world.width * settings.block_width - settings.width
            if g.camera_x > end_world:
                g.camera_x = end_world
        
    elif g.player.rect[0] < settings.width/4:
        delta = (1.0 - multiplier) * settings.camera_speed
        if delta >= 1:
            g.camera_x -= delta
            if g.camera_x < 0:
                g.camera_x = 0
    
    multiplier = g.player.rect[1]/float(settings.height)
    if g.player.rect[1] > settings.height * (2/3):
        delta = multiplier * settings.camera_speed
        if delta >= 1:
            g.camera_y += delta
            end_world = g.world.height * settings.block_width - settings.height
            if g.camera_y > end_world:
                g.camera_y = end_world
    
    elif g.player.rect[1] < settings.height/3:
        delta = (1.0 - multiplier) * settings.camera_speed
        if delta >= 1:
            g.camera_y -= delta
            if g.camera_y < 0:
                g.camera_y = 0

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
                if g.state_playing:
                    g.world.animation_update()
                    
                    if g.mushroom_time > 1:
                        mushroom_time = 1
                    elif g.mushroom_time < 1:
                        # will take 5 seconds to get back to 1
                        g.mushroom_time += 0.006666666
        
        if g.state_end_game:
            display_end_game_splash(screen)
        if g.state_playing:
            #print dt
            #print g.mushroom_time
            if g.mushroom_time < 1:
                dt *= g.mushroom_time
            #print dt
            #print
            g.world.update(dt)
            g.player.update(dt)
            
            reset_level = False
        
            # Did the player touch a monster?
            hits = pygame.sprite.spritecollide(g.player, g.world.monsters, False)
            for monster in hits:
                reset_level = True
            
            # Did the player get a goal?
            hits = pygame.sprite.spritecollide(g.player, g.world.goals, False)
            for goal in hits:
                g.world.goals.remove(goal)
                if len(g.world.goals) <= 0:
                    g.level += 1
                    reset_level = True
                else:
                    g.mushroom_time = 0.0

            if reset_level:
                load_world()
            else:
                screen.blit(bg, (0, 0))
                g.world.draw(screen)
                g.player.draw(screen)
                draw_score(screen)
                draw_fps(screen, dt)
                
                update_camera_offsets()
        
        pygame.display.flip()
                        
if __name__ == '__main__': main()

