import pygame

from utils.assets import HOLE

class Hole:
    
    def __init__(self, win: pygame.Surface, x: int, y: int):
        self.win = win
        self.x = x
        self.y = y

    def draw(self):
        self.win.blit(HOLE, (self.x*64, self.y*64))