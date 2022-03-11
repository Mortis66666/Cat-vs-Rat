import pygame
from .base_sprite import BaseSprite
from utils.assets import load


class Cat(BaseSprite):

    def __init__(self, win: pygame.Surface, x, y):
        super().__init__(win, x, y)


    @property
    def image(self):
        return pygame.transform.scale(
            load(
                f"Cat_{self}"
            ),
            (64, 64)
        )
