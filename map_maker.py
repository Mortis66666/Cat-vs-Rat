import random
import pygame
import json
import os

from main import Game, Cat, Rat, Box, win
from utils import map_name, BG, TOOLBAR



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

        map_id = ""

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
                                        "Rats": []
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
    occupied = []

    def __init__(self, map_id, /):
        self.map_id = map_id
        super().__init__(f"maps/map_{map_id}.json")
        
        pygame.display.set_caption(f"map_{map_id}")


    def extra_draw(self):
        if self.selected:
            self.selected.draw()

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

        elif pressed[pygame.K_c] and (x, y) not in self.occupied:
            self.cats.append(Cat(win, x, y))
            self.occupied.append((x, y))

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")

        elif pressed[pygame.K_r] and (x, y) not in self.occupied:
            self.rats.append(Rat(win, x, y))
            self.occupied.append((x, y))

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")

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

            try:
                self.occupied.remove((x, y))
            except:
                pass

            pygame.display.set_caption(f"map_{self.map_id} · Not saved")

        elif (pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]) and pressed[pygame.K_s]:
            self.save()

    def unique(self, seq: list):
        res = []
        for pos in seq:
            if pos not in res:
                res.append(pos)

        return res

    def handle(self):
        pass


    def save(self):
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
                    ]
                },
                file,
                indent=4
            )
        pygame.display.set_caption(f"map_{self.map_id} · Saved")



if __name__ == "__main__":
    choose = Choose()
    choose.start()

    choice = choose.choice

    if choice != -69:
        maker = Maker(choice)
        maker.start()

    else:
        pygame.quit()