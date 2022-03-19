
""" Map Maker

Use this file to make a map yourself!

Controls
--------
Click    -    Select the area
C key    -    Place a cat on the selected area
R key    -    Place a rat on the selected area
B key    -    Place a box on the selected area
CTRL + S -    Save the map


How to run?

Type python map_maker.py in command line to run the code

You can also do

python map_maker.py --map <id>

To instantly edit the map with the id you provide

"""

import random
import pygame
import json
import os
import argparse

from main import Game, Cat, Rat, Box, Tomato, Hole, Spike, win
from tkinter import messagebox
from sprites.base_sprite import BaseSprite
from utils import BG, TOOLBAR, CURSOR



RED = (255, 0, 0)
font = pygame.font.Font("Assets/font.ttf", 72)

class Selected:

    def __init__(self, win: pygame.Surface, x, y) -> None:
        self.x = x
        self.y = y

        self.win = win

    def draw(self):

        pygame.draw.rect(
            self.win,
            RED,
            (self.x * 64, self.y * 64, 64, 64),
            3
        )


class Choose:

    choice = ""
    submit = pygame.USEREVENT + 1

    def __init__(self) -> None:
        self.colors = [
            self.color
            for _ in range(3)
        ]

        while self.colors[0] == self.colors[1] or self.colors[0] == self.colors[2] or self.colors[2] == self.colors[1]:
            self.colors = [
                self.color
                for _ in range(3)
            ]

    def draw(self):
        
        word = font.render("Type the map id", True, self.colors[0])
        word2 = font.render("that you want to edit below", True, self.colors[1])
        word3 = font.render("Press enter to submit", True, self.colors[2])
        id = font.render(self.choice, True, "red")

        self.draw_background()
        win.blit(word, (win.get_width()//2 - word.get_width()//2, win.get_height()//2 - word.get_height()//2 - word2.get_height() - 100))
        win.blit(word2, (win.get_width()//2 - word2.get_width()//2, win.get_height()//2 - word2.get_height()//2 - 100))
        win.blit(TOOLBAR, (win.get_width()//2 - TOOLBAR.get_width()//2, win.get_height()//2 - TOOLBAR.get_height()//2 + 40))
        win.blit(id, (win.get_width()//2 - TOOLBAR.get_width()//2 + 20, win.get_height()//2 - TOOLBAR.get_height()//2 + 40))
        win.blit(word3, (win.get_width()//2 - word3.get_width()//2 + 20, win.get_height()//2 - TOOLBAR.get_height()//2 + 40 + word3.get_height()))

        pygame.display.update()

    def draw_background(self):
        for x in range(5):
            for y in range(5):
                win.blit(BG, (x*256, y*128))

    def next_index(self):
        return int(os.listdir("maps")[-1].split(".")[0].split("_")[-1]) + 1

    def post(self):
        pygame.event.post(
            pygame.event.Event(
                self.submit
            )
        )

    @property
    def color(self):
        return random.choice(("blue", "purple", "orange", "yellow", "green", "cyan"))

    def start(self):

        fps = 60
        clock = pygame.time.Clock()
        run = True


        pygame.display.set_caption("Choose a map")

        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.choice = -69
                    self.post()

                elif event.type == pygame.KEYDOWN:
                    c = pygame.key.name(event.key)
                    if c.isdigit():
                        self.choice += c

                    elif c == "backspace":
                        self.choice = self.choice[:-1]

                    elif c == "return":
                        self.post()

                    else:
                        pressed = pygame.key.get_pressed()

                        if (pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]) and pressed[pygame.K_n]:
                            index = self.next_index()
                            
                            with open(f"maps/map_{index}.json", "w") as file:
                                json.dump(
                                    {
                                        "Boxes": [],
                                        "Cats": [],
                                        "Rats": [],
                                        "Tomatoes": [],
                                        "Spikes": [],
                                        "Holes": []
                                    },
                                    file
                                )

                            self.choice = index
                            self.post()

                elif event.type == self.submit:
                    run = False
                    self.choice = int(self.choice)

                else:
                    self.draw()

class Maker(Game):

    selected: Selected | None = None

    def __init__(self, map_id, /):
        self.map_id = map_id
        self.history = []
        self.unsave = False
        super().__init__(f"maps/map_{map_id}.json", False)

        self.occupied = [
            (obj.x, obj.y)
            for obj in (self.cats + self.rats + self.boxes + self.tomatoes + self.holes)
        ]

        for hole in self.holes:
            self.occupied.append((hole.x+1, hole.y))
        
        pygame.display.set_caption(f"map_{map_id}")
        pygame.mouse.set_visible(False)


    def extra_draw(self):
        if self.selected:
            self.selected.draw()

        pos = pygame.mouse.get_pos()
        win.blit(CURSOR, pos)

    def handle_click(self):
        x, y = pygame.mouse.get_pos()
        self.selected = Selected(win, x//64, y//64)

    def handle_key(self):
        if not self.selected:
            return
        pressed = pygame.key.get_pressed()
        x, y = self.selected.x, self.selected.y

        if pressed[pygame.K_b] and (x, y) not in self.occupied:
            self.boxes.append(Box(win, x, y))
            self.occupied.append((x, y))

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")
            self.unsave = True

        elif pressed[pygame.K_c] and (x, y) not in self.occupied:
            self.cats.append(Cat(win, x, y))
            self.occupied.append((x, y))

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")
            self.unsave = True

        elif pressed[pygame.K_r] and (x, y) not in self.occupied:
            self.rats.append(Rat(win, x, y))
            self.occupied.append((x, y))

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")
            self.unsave = True

        elif pressed[pygame.K_t] and (x, y) not in self.occupied:
            self.tomatoes.append(Tomato(win, x, y))
            self.occupied.append((x, y))

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")
            self.unsave = True

        elif pressed[pygame.K_h] and (x, y) not in self.occupied and (x+1, y) not in self.occupied and x < 19:
            self.holes.append(Hole(win, x, y))
            self.occupied.append((x, y))
            self.occupied.append((x+1, y))

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")
            self.unsave = True

        elif pressed[pygame.K_d] or pressed[pygame.K_BACKSPACE] or pressed[pygame.K_DELETE]:
            for obj in self.cats:
                if (obj.x, obj.y) == (x, y):
                    self.cats.remove(obj)
            for obj in self.rats:
                if (obj.x, obj.y) == (x, y):
                    self.rats.remove(obj)
            for obj in self.boxes:
                if (obj.x, obj.y) == (x, y):
                    self.boxes.remove(obj)
            for obj in self.tomatoes:
                if (obj.x, obj.y) == (x, y):
                    self.tomatoes.remove(obj)
            for obj in self.spikes:
                if (obj.x, obj.y) == (x, y):
                    self.spikes.remove(obj)
            for obj in self.holes:
                if (obj.x, obj.y) == (x, y):
                    self.holes.remove(obj)
                    self.occupied.remove((x+1, y))
                elif (obj.x+1, obj.y) == (x, y):
                    self.holes.remove(obj)
                    self.occupied.remove((x-1, y))


            try:
                self.occupied.remove((x, y))
                pygame.display.set_caption(f"map_{self.map_id} · Not saved")
                self.unsave = True
            except ValueError:
                pass

        elif pressed[pygame.K_UP] and y:
            self.selected.y -= 1
        
        elif pressed[pygame.K_DOWN] and y < 9:
            self.selected.y += 1

        elif pressed[pygame.K_LEFT] and x:
            self.selected.x -= 1

        elif pressed[pygame.K_RIGHT] and x < 19:
            self.selected.x += 1

        elif (pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]) and pressed[pygame.K_s]:
            self.save()

        elif (pressed[pygame.K_s]) and (x, y) not in self.occupied:
            self.spikes.append(Spike(win, x, y))
            self.occupied.append((x, y))

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")
            self.unsave = True


    def unique(self, seq: list) -> list[BaseSprite]:
        res = []
        for pos in seq:
            if pos not in res:
                res.append(pos)

        return res

    def handle(self):
        pass

    def handle_event(self, event: pygame.event.Event, run: bool, again) -> bool:
        if event.type == pygame.QUIT:
            quit = True
            if self.unsave:
                quit = messagebox.askyesno(message="You have unsaved changes, are you sure you want to quit?")
            if quit:
                run = False
                pygame.quit()

        elif event.type == pygame.KEYDOWN:
            self.handle_key()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()

        return run, again



    def save(self):
        if len(self.holes) == 1:
            messagebox.showinfo(title="Can't save", message="Must place at least two holes")

        elif len(self.holes) > 2:
            messagebox.showinfo(title="Can't save", message="Cannot place more than two holes")

        else:
            with open(f"maps/map_{self.map_id}.json", "w") as file:
                json.dump(
                    {
                        "Boxes": [
                            [
                                box.x, box.y
                            ] for box in self.unique(self.boxes)
                        ],
                        "Cats": [
                            [
                                cat.x, cat.y
                            ] for cat in self.unique(self.cats)
                        ],
                        "Rats": [
                            [
                                rat.x, rat.y
                            ] for rat in self.unique(self.rats)
                        ],
                        "Tomatoes": [
                            [
                                tomato.x, tomato.y
                            ] for tomato in self.unique(self.tomatoes)
                        ],
                        "Holes": [
                            [
                                hole.x, hole.y
                            ] for hole in self.unique(self.holes)
                        ],
                        "Spikes": [
                            [
                                spike.x, spike.y
                            ] for spike in self.spikes
                        ]
                    },
                    file,
                    indent=4
                )
            pygame.display.set_caption(f"map_{self.map_id} · Saved")
            self.unsave = False


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--map", nargs="?", const=1, type=int, default=None)

    args = parser.parse_args()

    choice = args.map

    if not choice:
        choose = Choose()
        choose.start()

        choice = choose.choice

    if choice != -69:
        maker = Maker(choice)
        maker.start()

    else:
        pygame.quit()



if __name__ == "__main__":
    main()