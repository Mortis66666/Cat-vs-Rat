import pygame

from utils.assets import load
from utils.enums import spiky


class Spike:
    
    def __init__(self, win: pygame.Surface, x: int, y: int):
        self.win = win
        self.x = x
        self.y = y

        self.form = spiky.ACTIVE

    def change_form(self):
        self.form = spiky.INACTIVE if self.form == spiky.ACTIVE else spiky.ACTIVE

        return self

    @property
    def image(self):
        return pygame.transform.scale(load("Spikes" + ["", "_Active"][self.form == spiky.ACTIVE]), (64, 64))

    def draw(self):
        self.win.blit(self.image, (self.x*64, self.y*64))
    