import pygame
from enums import direction


class BaseSprite:

    def __init__(self, win: pygame.Surface, x: int, y: int):
        self.win = win
        self.x = x
        self.y = y

        self.facing = direction.DOWN


    def __str__(self):
        return str(self.facing).split(".")[1].capitalize()


    def draw(self):
        self.win.blit(self.image, (self.x*64, self.y*64))

    
    def move(self):

        match self.facing:

            case direction.UP:
                self.y -= 1

            case direction.DOWN:
                self.y += 1

            case direction.LEFT:
                self.x -= 1

            case direction.RIGHT:
                self.x += 1
    
    def handle(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.facing = direction.UP 

        elif pressed[pygame.K_DOWN]:
            self.facing = direction.DOWN

        elif pressed[pygame.K_LEFT]:
            self.facing = direction.LEFT

        elif pressed[pygame.K_RIGHT]:
            self.facing = direction.RIGHT