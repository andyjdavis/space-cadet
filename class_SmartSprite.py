import pygame

from lib import *
from class_MySprite import *

class SmartSprite(MySprite):
    def __init__(self, pos, vel, settings, g):
        MySprite.__init__(self, pos, vel, settings, g)
        
        self._future_pos = None
        self._future_vel = None
    
    def get_pos(self):
        if self._future_pos != None:
            return self._future_pos
        else:
            return self._pos
    
    def get_vel(self):
        if self._future_vel != None:
            return self._future_vel
        else:
            return self._vel
    
    def confirm_future(self):
        self._pos = self._future_pos
        self._future_pos = None
