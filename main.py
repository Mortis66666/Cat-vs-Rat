import pygame
import random
import json
import time

from abc import abstractmethod
from sprites import Cat, Rat, Box, Tomato
from sprites.base_sprite import BaseSprite
from utils.countdown import Coundown
from utils.enums import sprite
from utils import BG, ICON, MUSIC, map_name


pygame.init()


width, height = 1280, 640
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cat vs Rat")
pygame.display.set_icon(ICON)


# Colours
WHITE = (233, 233, 233)
BLACK = (0, 0, 0)



class Game:

    def __init__(self, f=map_name):

        self.cats = [
            Cat(win, x, y)
            for x, y in self.load("cats", f)
        ]

        self.rats = [
            Rat(win, x, y)
            for x, y in self.load("rats", f)
        ]

        self.boxes = [
            Box(win, x, y)
            for x, y in self.load("boxes", f)
        ]

        self.tomatoes = [
            Tomato(win, x, y)
            for x, y in self.load("tomatoes", f)
        ]

        self.last_update = 0


    def obstacles(self, *, cat=False) -> list[BaseSprite]:
        return [
            (box.x, box.y)
            for box in self.boxes
        ] + (
                [
                    (obj.x, obj.y)
                    for obj in self.rats
                ] if not cat else [
                    (obj.x, obj.y)
                    for obj in self.cats
                ]
            )

    def draw(self): # the draw function
        self.draw_background()

        lst = self.cats + self.rats + self.boxes + self.tomatoes

        for object in lst:
            object.draw()

        self.extra_draw()
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

        foo = random.randint(0, 1)

        if foo:
            for cat in self.cats:
                cat.eat(self.rats)
            for rat in self.rats:
                rat.eat(self.tomatoes)
        else:
            for rat in self.rats:
                rat.eat(self.tomatoes)
            for cat in self.cats:
                cat.eat(self.rats)

        for rat in self.rats:
            if not rat.alive and time.time() - rat.dead_time > rat.disappear_time:
                self.rats.remove(rat)

        for tomato in self.tomatoes:
            if tomato.eaten:
                self.tomatoes.remove(tomato)


    @abstractmethod
    def handle_click(self):
        pass

    def handle_event(self, event: pygame.event.Event, run: bool) -> bool:
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            self.handle_key()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()

        return run

    def load(self, name: str, f=map_name):

        with open(f, "r") as file:
            data = json.load(file)

        return data[name.title()]

    def start(self):

        # In game data
        run = True

        clock = pygame.time.Clock()
        fps = 60 # Frame per second

        pygame.mixer.music.load(MUSIC)
        pygame.mixer.music.play(-1)

        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                run = self.handle_event(event, run)

            if run:
                self.handle()
                self.draw()


def main():
    countdown = Coundown(win)
    countdown.start()

    game = Game()
    game.start()


if __name__ == "__main__":
    main()
