# This is a game called "Space Cadet".
#
# Space Cadet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Space Cadet is distributed in the hope that it will be useful and maybe even fun,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Space Cadet.  If not, see <http://www.gnu.org/licenses/>.
#
# copyright  2013 onwards Andrew Davis
# license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later

import os, pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

import math
import random

from lib import *
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
        self.background_color = (135, 206, 250)
        
        self.splash_size = (600, 400)
        self.text_antialias = 1
        self.text_color = (0, 0, 0)
        #self.text_bg_color = (0, 0, 0)
        
        self.mushroom_sound = None
        self.killed_sound = None
        
    def init_sound(self):
        self.mushroom_sound = load_sound("mushroom.ogg")
        self.killed_sound = load_sound("zap.ogg")
settings = Settings()

class Globals:
    def __init__(self):
        self.level = 5
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
pygame.display.set_caption('Space Cadet')
#pygame.mouse.set_visible(0)

settings.init_sound()

soundtrack_path = os.path.join('resources', 'music.mp3')
pygame.mixer.music.load(soundtrack_path)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

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

def update_camera_offsets(dt):

    x = g.player.rect[0] + (g.player.width/2)
    y = g.player.rect[1] + (g.player.height/2)

    multiplier = g.player.rect[0]/float(settings.width)
    if x > settings.width/2 + 20:
        delta = multiplier * dt * settings.player_move_acc
        if delta >= 1:
            g.camera_x += delta
            end_world = g.world.width * settings.block_width - settings.width
            if g.camera_x > end_world:
                g.camera_x = end_world
        
    elif x < settings.width/2 - 20:
        delta = (1.0 - multiplier) * dt * settings.player_move_acc
        if delta >= 1:
            g.camera_x -= delta
            if g.camera_x < 0:
                g.camera_x = 0
    
    multiplier = g.player.rect[1]/float(settings.height)
    if y > settings.height/2 + 20:
        delta = multiplier * dt * settings.player_move_acc
        if delta >= 1:
            g.camera_y += delta
            end_world = g.world.height * settings.block_width - settings.height
            if g.camera_y > end_world:
                g.camera_y = end_world
    
    elif y < settings.height/2 - 20:
        delta = (1.0 - multiplier) * dt * settings.player_move_acc
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
                settings.killed_sound.play()
                reset_level = True
            
            # Did the player get a goal?
            hits = pygame.sprite.spritecollide(g.player, g.world.goals, False)
            for goal in hits:
                settings.mushroom_sound.play()
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
                
                update_camera_offsets(dt)
        
        pygame.display.flip()
                        
if __name__ == '__main__': main()

