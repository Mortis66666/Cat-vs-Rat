import pygame

from utils.assets import TOMATO

class Tomato:
    
    def __init__(self, win: pygame.Surface, x: int, y: int):
        self.win = win
        self.x = x
        self.y = y

        self.eaten = False

    def draw(self):
        self.win.blit(TOMATO, (self.x*64, self.y*64))

    def eat(self):
        self.eaten = True