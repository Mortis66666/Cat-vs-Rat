import pygame
import random

from utils.assets import load
from utils.enums import spiky


class Spike:
    
    def __init__(self, win: pygame.Surface, x: int, y: int):
        self.win = win
        self.x = x
        self.y = y

        self.change_form()

    def change_form(self):
        self.form = random.choice(
            spiky.ACTIVE,
            spiky.INACTIVE
        )

    @property
    def image(self):
        return load("Spikes" + ["", "_Active"][self.form == spiky.ACTIVE])

    def draw(self):
        self.win.blit(self.image, (self.x*64, self.y*64))
    