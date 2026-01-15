import pygame
import os
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

IMAGE_PATH = "imgs"

IMAGE_MAPPINGS = {
    "outline": "n64.png"
}

def create_image(item):
    return pygame.image.load(os.path.join(IMAGE_PATH, IMAGE_MAPPINGS[item]))
class Display:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.width = screen_width
        self.height = screen_height
        pygame.display.set_caption("Video Game MIDI Controller")

    def write_text(self, text):
        font = pygame.font.SysFont('ocraextended',30)
        alert = font.render(text, 1, WHITE)
        self.screen.blit(alert, (0, 0))
        pygame.display.flip()

    def update_state(self, state):
        outline = create_image("outline")
        print(outline)
        self.screen.blit(outline, outline.get_rect(center = self.screen.get_rect().center))
        pygame.display.flip()

    def clear(self):
        self.screen.fill(BLACK)
        pygame.display.flip()


    


