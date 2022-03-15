import pygame

from .base_sprite import BaseSprite

class Hole:
    
    def __init__(self, win: pygame.Surface, x: int, y: int):
        self.win = win
        self.x = x
        self.y = y

    def occupied(self, objects: list[BaseSprite]) -> bool:
        for obj in objects:
            if obj.x == self.x and obj.y == self.y:
                return True

        return False

    def draw(self):
        pass