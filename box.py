from assets import BOX
import pygame

class Box:

    def __init__(self, win: pygame.Surface, x, y):
        self.win = win
        self.x = x
        self.y = y

    def draw(self):
        self.win.blit(BOX, (self.x*128, self.y*128))
