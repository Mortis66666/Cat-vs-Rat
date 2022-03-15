import pygame
from utils.enums import direction, sprite
from abc import abstractproperty

class BaseSprite:

    def __init__(self, win: pygame.Surface, x: int, y: int, _type: sprite=sprite.CAT):
        self.win = win
        self.x = x
        self.y = y

        self.facing = direction.DOWN
        self._type = _type


    @abstractproperty
    @property
    def image(self):
        pass


    def __str__(self):
        return str(self.facing).split(".")[1].capitalize()


    def draw(self):
        self.win.blit(self.image, (self.x*64, self.y*64))

    
    def move(self, obstacles):

        n = 0.2 if self._type == sprite.CAT else 0.5


        max_up = self.y
        max_down = 9 - self.y
        max_left = self.x
        max_right = 19 - self.x

        for x, y in obstacles:
            
            if abs(y - self.y) < 0.6:
                if x < self.x: # Left
                    max_left = min(max(self.x - (x+1), 0), max_left)
                elif x > self.x: # Right
                    max_right = min(max((x-1) - self.x, 0), max_right)

            if abs(x - self.x) < 0.6:
                if y < self.y: # Up
                    max_up = min(max(self.y - (y+1), 0), max_up)
                elif y > self.y: # Down
                    max_down = min(max((y-1) - self.y, 0), max_down)


        match self.facing:

            case direction.UP:
                self.y -= min(n, max_up)

            case direction.DOWN:
                self.y += min(n, max_down)

            case direction.LEFT:
                self.x -= min(n, max_left)

            case direction.RIGHT:
                self.x += min(n, max_right)
    
    def handle(self):

        pressed = pygame.key.get_pressed()

        if self._type == sprite.CAT:

            if pressed[pygame.K_UP]:
                self.facing = direction.UP 

            elif pressed[pygame.K_DOWN]:
                self.facing = direction.DOWN

            elif pressed[pygame.K_LEFT]:
                self.facing = direction.LEFT

            elif pressed[pygame.K_RIGHT]:
                self.facing = direction.RIGHT

        else:
            if pressed[pygame.K_w]:
                self.facing = direction.UP 

            elif pressed[pygame.K_s]:
                self.facing = direction.DOWN

            elif pressed[pygame.K_a]:
                self.facing = direction.LEFT

            elif pressed[pygame.K_d]:
                self.facing = direction.RIGHT