from main import Game, Cat, Rat, Box, win
from utils import map_name
import pygame
import json



RED = (255, 0, 0)


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


class Maker(Game):

    selected: Selected | None = None
    occupied = []


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
        with open(map_name, "w") as file:
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
    maker = Maker()
    maker.start()