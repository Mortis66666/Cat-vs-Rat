import pygame
from .base_sprite import BaseSprite
from utils.assets import load


class Rat(BaseSprite):

    def __init__(self, win: pygame.Surface, x, y):
        super().__init__(win, x, y)
        self.alive = True


    @property
    def image(self):
        return pygame.transform.scale(
            load(
                f"Mouse_{self}"
            ),
            (64, 64)
        )

    def __str__(self):
        return super().__str__() if self.alive else "Dead"