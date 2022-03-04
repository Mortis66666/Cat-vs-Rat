import pygame
import random
import json
from sprites import Cat, Rat, Box
from assets import BG


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

    def draw(self): # the draw function
        self.draw_background()
        self.extra_draw()

        lst = self.cats + self.rats + self.boxes

        random.shuffle(lst)

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
                self.draw()






if __name__ == "__main__":
    game = Game()
    game.start()
