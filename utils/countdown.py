import pygame
import time

from .assets import BG, load_music

pygame.init()

font = pygame.font.Font("Assets/font.ttf", 200)

class Coundown:

    def __init__(self, win: pygame.Surface, sound: bool):
        self.win = win
        self.sound = sound

    def draw_background(self):
        for x in range(5):
            for y in range(5):
                self.win.blit(BG, (x*256, y*128))

    def draw(self, n):
        self.draw_background()

        num = font.render(str(n), True, "black")

        self.win.blit(
            num,
            (
                self.win.get_width() // 2 - num.get_width() // 2,
                self.win.get_height() // 2 - num.get_height() // 2
            )
        )

        pygame.display.update()


    def start(self):
        if self.sound:
            pygame.mixer.music.load(load_music("countdown"))
            pygame.mixer.music.play()
        for i in range(3, -1, -1):
            if i:
                self.draw(i)
            else:
                self.draw("GO!")
            time.sleep(1)