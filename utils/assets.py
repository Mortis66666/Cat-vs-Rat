import os
import pygame

def load(image: str):
    return pygame.image.load(
        os.path.join(
            "Assets", image + ".png"
        )
    )


BG = load("Bg")
BOX = pygame.transform.scale(
    load("Box"),
    (64, 64)
)