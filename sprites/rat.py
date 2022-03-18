import pygame
import time
import random

from .base_sprite import BaseSprite
from .tomato import Tomato
from utils.assets import load
from utils.enums import sprite


class Rat(BaseSprite):

    def __init__(self, win: pygame.Surface, x, y):
        super().__init__(win, x, y, sprite.RAT)
        self.dead_time = 0
        self.disappear_time = random.randint(3, 7)

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

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False
        self.dead_time = time.time()

    def eat(self, tomatoes: list[Tomato]):
        for tomato in tomatoes:
            if abs(tomato.x - self.x) < 0.5 and abs(tomato.y - self.y) < 0.5:
                tomato.eat()