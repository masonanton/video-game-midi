import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Display:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        pygame.display.set_caption("Video Game MIDI Controller")

    def write_text(self, text):
        font = pygame.font.SysFont('ocraextended',30)
        alert = font.render(text, 1, WHITE)
        self.screen.blit(alert, (0, 0))
        pygame.display.flip()

    def clear(self):
        self.screen.fill(BLACK)
        pygame.display.flip()


