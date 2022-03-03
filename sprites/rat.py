import pygame
import os
from .base_sprite import BaseSprite


class Rat(BaseSprite):

    def __init__(self, win: pygame.Surface, x, y):
        super().__init__(win, x, y)


    @property
    def image(self):
        return pygame.transform.scale(
            pygame.image.load(
                os.path.join(
                    "Assets", f"Mouse_{self}.png"
                )
            ),
            (64, 64)
        )