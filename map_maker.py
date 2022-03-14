from main import Game, Cat, Rat, Box, win
from utils import map_name
import pygame
import json
import os



RED = (255, 0, 0)
font = pygame.font.SysFont("comicsans", 50)

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

    choice = 0

    def draw(self):
        
        word = font.render("Choose a map id to edit", True, "black")

        win.fill((255, 255, 255))
        win.blit(word, (win.get_width()//2 - word.get_width()//2, win.get_height()//2 - word.get_height()//2))

        pygame.display.update()

    def next_index(self):
        return int(os.listdir("maps")[-1].split(".")[0].split("_")[-1]) + 1

    def start(self):

        fps = 60
        clock = pygame.time.Clock()

        while not self.choice:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.choice = -69

                elif event.type == pygame.KEYDOWN:
                    c = pygame.key.name(event.key)
                    if c.isdigit():
                        self.choice = int(c)

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

                else:
                    self.draw()

class Maker(Game):

    selected: Selected | None = None
    occupied = []

    def __init__(self, map_id, /):
        self.map_id = map_id
        super().__init__(f"maps/map_{map_id}.json")


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

        elif pressed[pygame.K_c] and (x, y) not in self.occupied:
            self.cats.append(Cat(win, x, y))
            self.occupied.append((x, y))

        elif pressed[pygame.K_r] and (x, y) not in self.occupied:
            self.rats.append(Rat(win, x, y))
            self.occupied.append((x, y))

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


if __name__ == "__main__":
    choose = Choose()
    choose.start()

    choice = choose.choice

    if choice != -69:
        maker = Maker(choice)
        maker.start()

    else:
        pygame.quit()