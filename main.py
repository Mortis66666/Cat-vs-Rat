import pygame
import random
import json
import time
import argparse

from abc import abstractmethod
from sprites import Cat, Rat, Box, Tomato, Hole, Spike
from sprites.base_sprite import BaseSprite
from utils.countdown import Coundown
from utils.enums import sprite
from utils import BG, ICON, MUSIC, TOOLBAR, map_name
from utils.exceptions import CantTeleportError


pygame.init()


width, height = 1280, 640
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cat vs Rat")
pygame.display.set_icon(ICON)


# Colours
WHITE = (233, 233, 233)
BLACK = (0, 0, 0)


# Events
CATWIN = pygame.USEREVENT + 1
RATWIN = pygame.USEREVENT + 2

# Font
font = pygame.font.Font("Assets/font.ttf", 72)
smaller_font = pygame.font.Font("Assets/font.ttf", 30)


class Game:

    def __init__(self, f: str=map_name, sound: bool = True):

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

        self.holes = [
            Hole(win, x, y)
            for x, y in self.load("holes", f)
        ]

        self.last_update = 0
        self.sound = sound


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
                    for obj in (self.cats + self.tomatoes)
                ]
            )

    def draw(self): # the draw function
        self.draw_background()

        lst = self.holes + self.cats + self.rats + self.boxes + self.tomatoes

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

        # Move / teleport
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
                obstacles = None

                if obj._type == sprite.RAT:
                    if obj.alive:
                        obstacles = self.obstacles()
                        obj.move(obstacles)
                else:
                    obstacles = self.obstacles(cat=True)
                    obj.move(obstacles)

                if obj.alive and self.holes:
                    hole_1, hole_2 = self.holes

                    if (abs(obj.x - hole_1.x) < 1 and abs(obj.y - hole_1.y) < 1) or (abs(obj.x - (hole_1.x + 1)) < 1 and abs(obj.y - hole_1.y) < 1):
                        try:
                            obj.teleport(hole_2, obstacles)
                        except CantTeleportError:
                            pass
                    elif (abs(obj.x - hole_2.x) < 1 and abs(obj.y - hole_2.y) < 1) or (abs(obj.x - (hole_2.x + 1)) < 1 and abs(obj.y - hole_2.y) < 1):
                        try:
                            obj.teleport(hole_1, obstacles)
                        except CantTeleportError:
                            pass

            self.last_update = now

        foo = random.randint(0, 1)

        # Cat eat rat / Rat eat tomato
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

        # Remove dead rats if times up
        for rat in self.rats:
            if not rat.alive and time.time() - rat.dead_time > rat.disappear_time:
                self.rats.remove(rat)

        # Remove eaten tomato
        for tomato in self.tomatoes:
            if tomato.eaten:
                self.tomatoes.remove(tomato)

        # Check if anyone won
        if not any(map(Rat.is_alive, self.rats)):
            pygame.event.post(
                pygame.event.Event(CATWIN)
            )

        elif not self.tomatoes:
            pygame.event.post(
                pygame.event.Event(RATWIN)
            )


    @abstractmethod
    def handle_click(self):
        pass

    def handle_event(self, event: pygame.event.Event, run: bool, again: bool = False) -> tuple[bool, bool]:
        """Handle event here!!!"""
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            self.handle_key()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()

        elif event.type in (CATWIN, RATWIN):
            win_msg = ["CAT", "RAT"][event.type == RATWIN] + " WIN!"
            go = True
            while go:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        run = False
                        go = False
                        pygame.quit()
                        break
                    elif ev.type == pygame.KEYDOWN:
                        pressed = pygame.key.get_pressed()

                        if pressed[pygame.K_p]:
                            run = False
                            again = True
                            go = False

                        elif pressed[pygame.K_q]:
                            go = False
                            again = False
                            run = False
                if go:
                    text = font.render(win_msg, True, "red")
                    text_2 = smaller_font.render("PLAY AGAIN (P)", True, "red")
                    text_3 = smaller_font.render("QUIT (Q)", True, "red")
                    win.blit(   # Cat win!
                        text,
                        (
                            width // 2 - text.get_width() // 2,
                            height // 2 - text.get_height() // 2 - 200
                        )                    
                    )

                    win.blit(
                        TOOLBAR,  # Toolbar left
                        (
                            width // 2 - TOOLBAR.get_width() // 2 - 300,
                            height // 2 - text.get_height() // 2  
                        )                 
                    )

                    win.blit(
                        TOOLBAR,   # Toolbar right
                        (
                            width // 2 - TOOLBAR.get_width() // 2 + 300,
                            height // 2 - text.get_height() // 2  
                        )                 
                    )

                    win.blit(
                        text_2,    # Play again
                        (
                            width // 2 - TOOLBAR.get_width() // 2 - 250,
                            height // 2 - text_2.get_height() // 2  
                        )                 
                    )

                    win.blit(
                        text_3,   # Quit
                        (
                            width // 2 - TOOLBAR.get_width() // 2 + 350,
                            height // 2 - text_3.get_height() // 2  
                        )                 
                    )
                    
                    pygame.display.update()

        return run, again

    def load(self, name: str, f=map_name):

        with open(f, "r") as file:
            data = json.load(file)

        return data[name.title()]

    def start(self):

        # In game data
        run = True
        again = None

        clock = pygame.time.Clock()
        fps = 60 # Frame per second

        if self.sound:
            pygame.mixer.music.load(MUSIC)
            pygame.mixer.music.play(-1)

        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                run, again = self.handle_event(event, run, again)
                if not run:
                    return again

            if run:
                self.handle()
                self.draw()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--map", nargs="?", const=1, type=int, default=None)
    parser.add_argument("--debug", action=argparse.BooleanOptionalAction)
    parser.add_argument("--sound", action=argparse.BooleanOptionalAction)
    parser.set_defaults(sound=True)

    args = parser.parse_args()

    arg = args.map
    name = map_name
    sound = args.sound

    if arg:
        name = f"maps/map_{arg}.json"

    if not parser.parse_args().debug:
        countdown = Coundown(win, sound)
        countdown.start()

    game = Game(name, sound)
    again = game.start()

    while again:
        if not parser.parse_args().debug:
            countdown = Coundown(win, sound)
            countdown.start()

        game = Game(name, sound)
        again = game.start()


if __name__ == "__main__":
    main()
