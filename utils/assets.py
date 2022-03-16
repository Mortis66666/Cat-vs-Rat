import os
import pygame

def load(image: str):
    return pygame.image.load(
        os.path.join(
            "Assets", image + ".png"
        )
    )

def load_music(music: str):
    return os.path.join("Assets", music + ".mp3")


BG = load("Bg")
BOX = pygame.transform.scale(
    load("Box"),
    (64, 64)
)
TOMATO = pygame.transform.scale(
    load("Tomato"),
    (64, 64)
)
HOLE = load("Hole")
ICON = pygame.transform.scale(
    load("Cat_Avatar_Rounded"),
    (32, 32)
)
TOOLBAR = load("UI_Toolbar")
CURSOR = load("Cursor_Point")
MUSIC = load_music("Music")