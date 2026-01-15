import pygame
import os
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

IMAGE_PATH = "imgs"

IMAGE_MAPPINGS = {
    "outline": "outline.png",
    "START": "start.png"
}

def create_image(item):
    return pygame.image.load(os.path.join(IMAGE_PATH, IMAGE_MAPPINGS[item]))
class Display:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.width = screen_width
        self.height = screen_height
        self.center = self.screen.get_rect().center
        pygame.display.set_caption("Video Game MIDI Controller")

    def write_text(self, text):
        font = pygame.font.SysFont('ocraextended',30)
        alert = font.render(text, 1, WHITE)
        self.screen.blit(alert, (0, 0))
        pygame.display.flip()

    def display_image(self, image):
        self.screen.blit(image, image.get_rect(center = self.center))

    def update_state(self, state):
        outline = create_image("outline")
        self.display_image(outline)
        print(state["buttons_on"])
        for button_name in state["buttons_on"]:
            button_image = create_image(button_name)
            self.display_image(button_image)
        pygame.display.flip()

    def clear(self):
        self.screen.fill(BLACK)
        pygame.display.flip()


    


