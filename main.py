import random
import pygame
from cat import Cat
from rat import Rat
from box import Box
from assets import BG
pygame.init()


width, height = 1280, 640
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cat vs Rat")


# Colours
WHITE = (233, 233, 233)
BLACK = (0, 0, 0)



class Game:

    cats: list[Cat] = []
    rats: list[Rat] = []

    def draw(self, boxes): # the draw function
        self.draw_background()

        lst = self.cats + self.rats

        random.shuffle(lst)

        for object in lst:
            object.draw()

        for box in boxes:
            box.draw()

        pygame.display.update()

    def draw_background(self):
        for x in range(5):
            for y in range(5):
                win.blit(BG, (x*256, y*128))

    def handle(self):
        lst = self.cats + self.rats
        random.shuffle(lst)

        for object in lst:
            object.handle()

    def start(self):

        for y in range(10):
            for x in range(20):
                self.cats.append(Cat(win, x, y))

        boxes = [Box(win, 3, 3), Box(win, 2, 3)]

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
                    self.handle()

            if run:
                self.draw(boxes)






if __name__ == "__main__":
    game = Game()
    game.start()
