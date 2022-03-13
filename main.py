import pygame
import random
import json
import time
from sprites import Cat, Rat, Box
from sprites.base_sprite import BaseSprite
from utils.assets import BG
from abc import abstractmethod
from utils.enums import sprite


pygame.init()


width, height = 1280, 640
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cat vs Rat")


# Colours
WHITE = (233, 233, 233)
BLACK = (0, 0, 0)



class Game:

    def __init__(self):

        self.cats = [
            Cat(win, x, y)
            for x, y in self.load("cats")
        ]

        self.rats = [
            Rat(win, x, y)
            for x, y in self.load("rats")
        ]

        self.boxes = [
            Box(win, x, y)
            for x, y in self.load("boxes")
        ]

        self.last_update = 0


    def obstacles(self, *, cat=False) -> list[BaseSprite]:
        return [
            (box.x, box.y)
            for box in self.boxes
        ] + (
                [
                    (obj.x, obj.y)
                    for obj in (self.rats + self.cats)
                ] if not cat else [
                    (obj.x, obj.y)
                    for obj in self.cats
                ]
            )

    def draw(self): # the draw function
        self.draw_background()
        self.extra_draw()

        lst = self.cats + self.rats + self.boxes

        for object in lst:
            object.draw()

        pygame.display.update()

    def draw_background(self):
        for x in range(5):
            for y in range(5):
                win.blit(BG, (x*256, y*128))

    def extra_draw(self):
        pass

    def handle_key(self):
        lst = self.cats + self.rats
        random.shuffle(lst)

        for object in lst:
            object.handle()


    def handle(self):
        pressed = pygame.key.get_pressed()

        cat = False
        rat = False

        if any((pressed[pygame.K_UP], pressed[pygame.K_DOWN], pressed[pygame.K_LEFT], pressed[pygame.K_RIGHT])):
            cat = True

        if any((pressed[pygame.K_w], pressed[pygame.K_s], pressed[pygame.K_a], pressed[pygame.K_d])):
            rat = True

        lst: list[BaseSprite] = []

        if cat:
            lst.extend(self.cats)

        if rat:
            lst.extend(self.rats)

        random.shuffle(lst)

        now = time.time()

        if now - 0.05 > self.last_update:
            for obj in lst:
                if obj._type == sprite.RAT:
                    if obj.alive:
                        obj.move(self.obstacles())
                else:
                    obj.move(self.obstacles(cat=True))
            self.last_update = now

        for cat in self.cats:
            cat.eat(self.rats)


    @abstractmethod
    def handle_click(self):
        pass

    def load(self, name: str):

        with open("map.json", "r") as file:
            data = json.load(file)

        return data[name.title()]

    def start(self):

        # In game data
        run = True

        clock = pygame.time.Clock()
        fps = 60 # Frame per second

        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                
                elif event.type == pygame.KEYDOWN:
                    self.handle_key()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click()

            if run:
                self.handle()
                self.draw()






if __name__ == "__main__":
    game = Game()
    game.start()
