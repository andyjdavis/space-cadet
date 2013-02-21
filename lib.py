import math, os, pygame
from pygame.locals import *

def update_pos(pos, delta):
    delta = int(round(delta, 0))
    return pos + delta

def sprite_on_tile(sprite, tile_pos):
    sprite.sitting_on = tile_pos
    sprite.vel[1] = 0
    sprite.pos[1] = tile_pos.pos[1] - g.settings.block_size/2 - sprite.size[1]/2

def load_image(name, colorkey=-1, perpixelalpha=False):
    fullname = os.path.join('resources', name)
    
    try:
        image = pygame.image.load(fullname)
        if perpixelalpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(settings.resourcepath, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound
