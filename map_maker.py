from main import Game, Cat, Rat, Box, win
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

    def extra_draw(self):
        if self.selected:
            self.selected.draw()

    def handle_click(self):
        x, y = pygame.mouse.get_pos()
        self.selected = Selected(win, x//64, y//64)

    def handle_key(self):
        pressed = pygame.key.get_pressed()
        x, y = self.selected.x, self.selected.y

        if pressed[pygame.K_b]:
            self.boxes.append(Box(win, x, y))

        elif pressed[pygame.K_c]:
            self.cats.append(Cat(win, x, y))

        elif pressed[pygame.K_r]:
            self.rats.append(Rat(win, x, y))

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



    def load(self, name: str):

        with open("map.json", "r") as file:
            data = json.load(file)

        return data[name.title()]


if __name__ == "__main__":
    maker = Maker()
    maker.start()